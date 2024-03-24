"""
Activities module
- create_activity: create activity descriptor
- create_readme: create README.md file for activity (including some questions rendered as images)
- has_quiz_files: check if activity has quiz files
- is_activity: check if a path is an activity (is a directory and has an activity descriptor or quiz files)
- read_activity: read activity descriptor
"""

import os
import shutil
import json
import xml.etree.ElementTree as ET

from jinja2 import Environment, FileSystemLoader

from actirepo.__init__ import __icons_url__, __download_url__
from actirepo.question import render_question
from actirepo.url_utils import normalize
from actirepo.file_utils import is_newer_than, anchorify
from actirepo.console import title, input_string, input_list

# default limit
LIMIT = 9999

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

# supported difficulties
DIFFICULTIES = [ 'easy', 'medium', 'hard' ]

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

def has_quiz_files(activity_path):
    """
    Check if activity has quiz files
    - activity_path: path to activity
    - returns: True if activity has quiz files, False otherwise
    """
    for file in os.listdir(activity_path):
        if is_quiz_file(os.path.join(activity_path, file)):
            return True
    return False

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
    try:
        tree = ET.parse(questions_file)
        # check if root is "quiz" tag 
        return tree.getroot().tag == 'quiz'
    except:
        return False

def is_activity(path):
    """
    Check if a path is an activity (is a directory and has an activity descriptor or quiz files)
    - path: path to activity
    - returns: True if path is an activity, False otherwise
    """
    return os.path.isdir(path) and (os.path.isfile(os.path.join(path, ACTIVITY_FILE)) or has_quiz_files(path))

def read_activity(activity_path, full = False):
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
        activity['description'] = ''
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
        activity['limit'] = LIMIT
    # if full is true, add questions to activity descriptor
    if full:
        activity['questions'] = _get_all_questions(activity)
        activity['total'] = sum([ file['total'] for file in activity['questions'] ])  
    return activity

# create README.md file for activity (including some questions rendered as images)
def create_readme_activity(activity, force = False):
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
        activity_files = [ ACTIVITY_FILE ]
        activity_files.extend(activity['files'])
        readme_is_old = True
        for file in activity_files:
            file = os.path.join(activity_path, file)
            if is_newer_than(file, readme_file):
                readme_is_old = False
                break
        if readme_is_old:
            print(f'Ignorando actividad "{activity_path}". README.md es más reciente que {ACTIVITY_FILE} y que los archivos de preguntas {activity["files"]}')
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

def create_activity(path, force = False):
    """
    Create activity descriptor
    - path: path to activity
    - force: if true, overwrite existing activity descriptor
    """
    activity_file = os.path.join(path, ACTIVITY_FILE)
    # check if activity descriptor exists and force is false
    if os.path.isfile(activity_file) and not force:
        raise Exception(f'{path} ya es una actividad. Use --force para sobreescribir')
    # if there is activity descriptor, reads it
    default_activity = read_activity(path)        
    # check if there are xml files
    if not has_quiz_files(path):
        raise Exception(f'No hay archivos de preguntas en {path}')
    # create activity descriptor
    activity = {
        'name': input_string('Nombre', default_activity['name']),
        'description': input_string('Descripción', default_activity['description']),
        'category': input_list('Categoría', default_activity['category']),
        'difficulty': input_string(f'Dificultad {DIFFICULTIES}', default_activity['difficulty']),
        'tags': input_list('Tags', default_activity['tags']),
        'author': {
            'name': input_string('Autor name', default_activity['author']['name'] if default_activity['author'] else os.environ.get('USER', os.environ.get('USERNAME'))),
            'email': input_string('Autor email', default_activity['author']['email'] if default_activity['author'] else '')
        },
        'limit': input_string('Límite de preguntas de cada tipo a mostrar en el README', default_activity['limit'])
    }
    # write activity descriptor to json file
    with open(activity_file, 'w') as outfile:
        json.dump(activity, outfile, indent=4)