import os
import shutil
import json
import xml.etree.ElementTree as ET

from jinja2 import Environment, FileSystemLoader

from actirepo.__init__ import __icons_url__, __download_url__
from actirepo.question import render_question
from actirepo.url_utils import normalize
from actirepo.file_utils import is_newer_than, anchorify
from actirepo.format_utils import title

# get module path
MODULE_PATH = os.path.dirname(os.path.realpath(__file__))

# load and render template
TEMPLATES_PATH = os.path.join(MODULE_PATH, 'templates')

# activity filename
ACTIVITY_FILE = 'activity.json'

# activity README template
README_TEMPLATE = 'README.activity.template.md'

# supported question types
SUPPORTED_TYPES = {
    'shortanswer':      'Respuesta corta',
    'multichoice':      'Opción múltiple',
    'truefalse':        'Verdadero/Falso',
    'matching':         'Emparejamiento',
    'cloze':            'Asociación',
    'ddimageortext':    'Arrastrar y soltar sobre una imagen',
    'ddmarker':         'Arrastrar y soltar marcadores',
    'essay':            'Ensayo',
    'numerical':        'Numérico'
}

# anchorified question types
ANCHORIFIED_TYPES = { key : anchorify(value) for key, value in SUPPORTED_TYPES.items() }

def _path_to_category(path):
    """
    Convert path to category
    - path: path to activity
    - returns: list of categories
    """
    parts = path.split(os.sep)
    return [ part.capitalize() for part in parts[0:len(parts)-1] ]

def _get_questions_from_file(activity_path, file):
    """
    Get questions from file
    - activity_path: path to activity
    - file: questions file
    - returns: list of questions organized by file and type
    """
    # get full path to questions file and parse xml
    questions_file = os.path.join(activity_path, file)
    tree = ET.parse(questions_file)
    # search "question" tags under "quiz" tag
    types = {}
    for question in tree.findall('question'):
        # get question type
        type = question.get('type')
        # skip if question type is not supported
        if not type in SUPPORTED_TYPES:
            continue
        # check if question type is in types dictionary, and add it if not
        if not type in types:
            types[type] = [ question ]
        else:
            types[type].append(question)
    # return questions
    return {
        'file': file,
        'url' : normalize(f'{__download_url__}/{activity_path}/{file}'),
        'types': types,
        'total': sum([len(type) for type in types.values()])
    }

def _get_all_questions(activity):
    """
    Get all questions from activity's question files
    - activity: activity descriptor
    - returns: list of questions organized by file and type
    """
    all_questions = []
    for file in activity['files']:
        all_questions.append(_get_questions_from_file(activity['path'], file))
    return all_questions

def _generate_images(activity, force = True):
    """
    Generate images for questions in activity
    - activity: activity descriptor
    - force: if true, overwrite existing images
    """
    images_dir = os.path.join(activity['path'], "images")
    # if images directory exists and force is true, delete it
    if os.path.isdir(images_dir) and force:
        print("Sobreescribiendo imágenes existentes")
        shutil.rmtree(images_dir)
    # walk through all question files in activity
    for questions_file in activity['questions']:
        # create images dictionary
        images = {}
        # walk through all questions in file
        for type,questions in questions_file['types'].items():
            count = 0
            # walk through all questions of the same type
            for question in questions:
                # render image for question
                image_file = render_question(question, images_dir)
                # if image was generated, add it to dictionary
                if image_file:
                    count += 1
                    # check if question type is in images dictionary, and add it if not
                    if not type in images:
                        images[type] = [ image_file ]
                    else:
                        images[type].append(image_file)
                if count >= activity['limit']:
                    break
        # add images to questions file  
        questions_file['images'] = images

def is_quiz_file(questions_file):
    """
    Check if a file is a quiz file
    - questions_file: path to questions file
    - returns: True if file is a quiz file, False otherwise
    """
    # check if file is an xml file
    if not questions_file.endswith('.xml'):
        return False
    # get full path to questions file and parse xml
    tree = ET.parse(questions_file)
    # check if root is "quiz" tag 
    return tree.getroot().tag == 'quiz'

def is_activity(path):
    """
    Check if a path is an activity
    - path: path to activity
    - returns: True if path is an activity, False otherwise
    """
    # check if path is a directory
    if os.path.isdir(path):
        # check if activity file exists
        if os.path.isfile(os.path.join(path, ACTIVITY_FILE)):
            return True
        # check if there are xml files in directory
        else:            
            for file in os.listdir(path):
                if is_quiz_file(os.path.join(path, file)):
                    return True
    return False

def read_activity(activity_path):
    """
    Read activity descriptor
    - activity_path: path to activity
    - returns: activity descriptor    
    """
    # get full path to activity descriptor
    activity_file = os.path.join(activity_path, ACTIVITY_FILE)
    # checks if activity descriptor exists
    if os.path.isfile(activity_file):
        # read activity descriptor
        with open(activity_file, 'r') as json_file:
            content = json_file.read()
        # parse activity descriptor
        activity = json.loads(content)
    else:
        # creates a new activity descriptor by default
        activity = {
            'name': os.path.basename(activity_path).capitalize(),
            'tags': []
        }
    # add path to activity descriptor
    activity['path'] = os.path.normpath(activity_path)
    # add description to activity descriptor if it is not present
    if not 'description' in activity:
        activity['description'] = 'Actividad sin descripción'
    # add difficulty to activity descriptor if it is not present
    if not 'difficulty' in activity:
        activity['difficulty'] = 'unknown'
    # add category to activity descriptor if it is not present
    if not 'category' in activity:
        activity['category'] = _path_to_category(activity['path'])
    # if there are no files in activity descriptor, get all files in activity path
    if not 'files' in activity:
        activity['files'] = [ file for file in os.listdir(activity_path) if file.endswith('.xml') and is_quiz_file(os.path.join(activity_path, file)) ]
    # if there is no limit in activity descriptor, set it to max int
    if not 'limit' in activity:
        activity['limit'] = 9999
    return activity

# create README.md file for activity (including some questions rendered as images)
def create_readme(activity, force = False):
    """
    Create README.md file for activity (including some questions rendered as images)
    - activity: activity descriptor
    - force: if true, overwrite existing README.md    
    """
    # get activity path
    activity_path = activity['path']
    # set readme and activity files
    readme_file = os.path.join(activity_path, 'README.md')
    # avoid creating README.md if it is not necessary
    if not force:
        # check if current README.md is newer than activity.json and question files, and skip if it is
        checked_files = [ ACTIVITY_FILE ].extend(activity['files'])
        readme_is_old = True
        for file in checked_files:
            file = os.path.join(activity_path, file)
            if is_newer_than(file, readme_file):
                readme_is_old = False
                break
        if readme_is_old:
            print(f'Ignorando actividad "{activity_path}". README.md es más reciente que {ACTIVITY_FILE} y que los archivos de preguntas {activity["questions"]}')
            return
    # print message
    title(f'Creando README.md para actividad en {activity_path}...')
    # get stats and add to metadata
    questions = _get_all_questions(activity)
    activity['questions'] = questions
    # generate images
    _generate_images(activity, force)
    # load and render template
    env = Environment(loader = FileSystemLoader(TEMPLATES_PATH, encoding='utf8'))
    template = env.get_template(README_TEMPLATE)
    readme = template.render(activity = activity, SUPPORTED_TYPES = SUPPORTED_TYPES, ANCHORIFIED_TYPES = ANCHORIFIED_TYPES, icons_url = __icons_url__)
    # write to file
    print("generando README.md: ", readme_file)
    with open(readme_file, 'w') as outfile:
        outfile.write(readme)