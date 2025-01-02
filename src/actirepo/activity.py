"""
Activities module
- create_activity: create activity descriptor
- create_readme: create README.md file for activity (including some questions rendered as images)
- has_quiz_files: check if activity has quiz files
- is_activity: check if a path is an activity (is a directory and has an activity descriptor or quiz files)
- read_activity: read activity descriptor
"""

import os
import json
import shutil

from jinja2 import Environment, FileSystemLoader
from pprint import pprint

from actirepo.__init__ import __icons_url__
from actirepo.utils.file_utils import is_newer_than, anchorify, path_to_capitalized_list
from actirepo.utils.console import title, input_string, input_list
from actirepo.artifact import Artifact
from actirepo.moodle.quiz import Quiz
from actirepo.moodle.stats import Stats

class Activity(Artifact):

    # default limit
    LIMIT = 9999

    # activity filename
    METADATA_FILE = 'activity.json'

    # activity README template
    README_TEMPLATE = 'README.activity.template.md'

    # supported difficulties
    DIFFICULTIES = [ 'easy', 'medium', 'hard' ]

    def __init__(self, path):
        super().__init__(path, self.METADATA_FILE)
        self.quizzes = self.__get_quizzes()

    def __get_quizzes(self):
        """
        Get quizzes in activity
        - returns: list of quizzes in activity
        """
        return [ Quiz(os.path.join(self.path, file)) for file in self.metadata['files'] ]

    def load(self):
        """
        Read activity descriptor
        - full: if true, adds stats to activity descriptor
        - returns: activity descriptor
        """
        # checks if activity descriptor exists
        if os.path.isfile(self.descriptor):
            # read activity descriptor
            with open(self.descriptor, 'r') as json_file:
                content = json_file.read()
            # parse activity descriptor
            self.metadata = json.loads(content)
        else:
            # creates a new activity descriptor by default
            self.metadata = {
                'name': self.name.capitalize(),
                'tags': []
            }
        # add description to activity descriptor if it is not present
        if not 'description' in self.metadata: self.metadata['description'] = ''
        # add difficulty to activity descriptor if it is not present
        if not 'difficulty' in self.metadata: self.metadata['difficulty'] = 'unknown'
        # add category to activity descriptor if it is not present
        if not 'category' in self.metadata: self.metadata['category'] = path_to_capitalized_list(self.path)
        # if there are no files in activity descriptor, get all files in activity path
        if not 'files' in self.metadata: self.metadata['files'] = [ file for file in os.listdir(self.path) if Quiz.is_quiz_file(os.path.join(self.path, file)) ]
        # if there is no limit in activity descriptor, set it to max int
        if not 'limit' in self.metadata: self.metadata['limit'] = Activity.LIMIT
        # if full is true, add questions to activity descriptor
        self.metadata['stats'] = self.__get_stats(self.metadata['files'])
        self.metadata['full_stats'] = self.get_stats()
        return self.metadata
    
    def save(self):
        """
        Save activity descriptor
        """
        with open(self.descriptor, 'w', encoding='utf-8') as outfile:
            json.dump(self.metadata, outfile, indent=4)

    def find_quizzes(self):
        """
        List quizzes in activity
        - returns: list of quizzes in moodle xml format
        """
        return [ file for file in os.listdir(self.path) if Quiz.is_quiz_file(os.path.join(self.path, file)) ]
    
    def __get_stats(self, files):
        """
        Get activity stats
        - returns: activity stats
        """
        stats = {}
        for file in files:
            quiz = Quiz(os.path.join(self.path, file))
            stats[file] = quiz.get_stats()
        return stats
    
    def get_stats(self):
        """
        Get activity total stats
        - returns: activity total stats
        """
        all_stats = self.metadata['stats'].values()
        result = Stats()
        for stats in all_stats:
            result += stats
        return result
    
    def is_upgradable(self):
        """
        Check if activity is upgradable
        - returns: True if activity is upgradable, False otherwise
        """
        activity_files = [ os.path.join(self.path, file) for file in [ Activity.METADATA_FILE ].extend(self.metadata['files']) ]
        return not is_newer_than(self.readme_file, activity_files)
    
    def __generate_images(self):
        # remove images folder if it exists
        images_dir = os.path.join(self.path, 'images')
        if os.path.isdir(images_dir):
            shutil.rmtree(images_dir)
        # generate images
        for quiz in self.quizzes:
            quiz.generate_images(self.metadata['limit'])

    # create README.md file for activity (including some questions rendered as images)
    def create_readme(self, force = False):
        """
        Create README.md file for activity (including some questions rendered as images)
        - force: if true, overwrite existing README.md    
        """
        # avoid creating README.md if it is not necessary
        if not force and not self.is_upgradable():
            print(f'Ignorando actividad "{self.path}". README.md es más reciente que {Activity.METADATA_FILE} y/o alguno de los archivos de preguntas {self.quizzes}')
            return
        # print message
        title(f'Creando README.md para actividad en {self.path}...')
        # generate images
        self.__generate_images()
        # load and render template
        env = Environment(loader = FileSystemLoader(self.TEMPLATES_PATH, encoding='utf8'))
        env.filters['anchorify'] = anchorify
        env.filters['debug'] = pprint
        env.filters['difficulty_to_badge'] = Activity.difficulty_to_badge
        template = env.get_template(self.README_TEMPLATE)
        readme = template.render(activity = self, icons_url = __icons_url__, Quiz = Quiz)
        # write to file
        print("generando README.md: ", self.readme_file)
        with open(self.readme_file, 'w', encoding='utf-8') as outfile:
            outfile.write(readme)

    @staticmethod
    def has_quiz_files(path):
        """
        Check if activity has quiz files
        - path: path to activity directory
        - returns: True if directory has quiz files, False otherwise
        """
        for file in os.listdir(path):
            if Quiz.is_quiz_file(os.path.join(path, file)):
                return True
        return False
    
    @staticmethod
    def is_activity(path):
        """
        Check if a path is an activity (is a directory and has an activity descriptor or quiz files)
        - path: path to activity
        - returns: True if path is an activity, False otherwise
        """
        if not os.path.isdir(path): 
            return False
        descriptor = os.path.join(path, Activity.METADATA_FILE)
        return os.path.isdir(path) and (os.path.isfile(descriptor) or Activity.has_quiz_files(path))

    @staticmethod    
    def create(path, force = False):
        """
        Create activity descriptor
        - path: path to activity
        - force: if true, overwrite existing activity descriptor
        """
        descriptor = os.path.join(path, Activity.METADATA_FILE)
        # check if activity descriptor exists and force is false
        if os.path.isfile(descriptor) and not force:
            raise Exception(f'{path} ya es una actividad. Use --force para sobreescribir')
        # if there is activity descriptor, loads it
        default_metadata = Activity(path).metadata
        # check if there are xml files
        if not Activity.has_quiz_files(path):
            raise Exception(f'No hay archivos de preguntas en {path}')
        # create activity descriptor
        activity = {
            'name': input_string('Nombre', default_metadata['name']),
            'description': input_string('Descripción', default_metadata['description']),
            'category': input_list('Categoría', default_metadata['category']),
            'difficulty': input_string(f'Dificultad {Activity.DIFFICULTIES}', default_metadata['difficulty']),
            'tags': input_list('Tags', default_metadata['tags']),
            'author': {
                'name': input_string('Autor name', default_metadata['author']['name'] if default_metadata['author'] else os.environ.get('USER', os.environ.get('USERNAME'))),
                'email': input_string('Autor email', default_metadata['author']['email'] if default_metadata['author'] else '')
            },
            'limit': input_string('Límite de preguntas de cada tipo a mostrar en el README', default_metadata['limit'])
        }
        # write activity descriptor to json file
        with open(descriptor, 'w', encoding='utf-8') as outfile:
            json.dump(activity, outfile, indent=4)

    @staticmethod
    def difficulty_to_string(diff):
        """
        Get difficulty levels
        """
        if not diff:
            return 'Sin especificar'
        if diff == 'easy':
            return 'Fácil'
        if diff == 'medium':
            return 'Medio'
        if diff == 'hard':
            return 'Difícil'
        return 'Desconocido'
    
    @staticmethod
    def difficulty_to_badge(diff):
        """
        Get difficulty badge
        """
        if not diff:
            return '![Dificultad](https://img.shields.io/badge/Dificultad-Sin%20especificar-black)'
        if diff == 'easy':
            return '![Dificultad](https://img.shields.io/badge/Dificultad-Baja-green)'
        if diff == 'medium':
            return '![Dificultad](https://img.shields.io/badge/Dificultad-Media-yellow)'
        if diff == 'hard':
            return '![Dificultad](https://img.shields.io/badge/Dificultad-Alta-red)'
        return '![Dificultad](https://img.shields.io/badge/Dificultad-Desconocida-black)'
