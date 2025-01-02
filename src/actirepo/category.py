import os
import json

from jinja2 import Environment, FileSystemLoader
from pprint import pprint

from actirepo.__init__ import __icons_url__
from actirepo.utils.file_utils import is_newer_than, anchorify, path_to_capitalized_list
from actirepo.utils.console import title, input_string, input_list
from actirepo.artifact import Artifact
from actirepo.activity import Activity
from actirepo.moodle.quiz import Quiz
from actirepo.moodle.stats import Stats

class Category(Artifact):

    METADATA_FILE = 'category.json'

    def __init__(self, path):
        super().__init__(path, self.METADATA_FILE)

    def __find_categories(self):
        """
        List subcategories in category
        - returns: list of subcategories in category
        """
        return [ Category(os.path.join(self.path, file)) for file in os.listdir(self.path) if Category.is_category(os.path.join(self.path, file)) ]

    def __find_activities(self):
        """
        List activities in category
        - returns: list of activities in category
        """
        return [ Activity(os.path.join(self.path, file)) for file in os.listdir(self.path) if Activity.is_activity(os.path.join(self.path, file)) ]    
   
    @staticmethod
    def is_category(path):
        """
        Check if a path is a category (is a directory and has a category descriptor or just folders)
        - path: path to category
        - returns: True if path is an category, False otherwise
        """
        if (not os.path.isdir(path)):
            return False
        descriptor = os.path.join(path, Category.METADATA_FILE)
        return (os.path.isfile(descriptor) or Category.__just_contains_folders(path))
    
    @staticmethod
    def __just_contains_folders(path):
        """
        Check if a path just contains folders
        """
        for dirs in os.listdir(path):
            if not os.path.isdir(dirs):
                return False
        return True
    
    def load(self):
        """
        Read category descriptor
        - returns: category descriptor
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
        # add category to activity descriptor if it is not present
        if not 'category' in self.metadata: self.metadata['category'] = path_to_capitalized_list(self.path)
        # add tags to activity descriptor if it is not present
        if not 'tags' in self.metadata: self.metadata['tags'] = []
        # find categories and activities
        self.activities = self.__find_activities()
        self.categories = self.__find_categories()
        # add stats to activity descriptor if it is not present
        if not 'stats' in self.metadata: self.metadata['stats'] = self.get_stats()
        return self.metadata
    
    def save(self):
        """
        Save activity descriptor
        """
        with open(self.descriptor, 'w') as outfile:
            json.dump(self.metadata, outfile, indent=4)

    def get_stats(self):
        """
        Get category full stats
        - returns: activity stats
        """
        result = Stats()
        for activity in self.activities:
            result += activity.get_stats()
        for category in self.categories:
            result += category.get_stats()
        return result

    def create_readme(self):
        """
        Create README.md file for category (including all activities in category and subcategories)
        - force: if true, overwrite existing README.md
        """
        # set readme file
        readme_file = os.path.join(self.path, 'README.md')
        # print message
        title(f'Creando README.md para categoría en {self.path}...')
        # load and render template
        env = Environment(loader = FileSystemLoader(self.TEMPLATES_PATH, encoding='utf8'))
        env.filters['anchorify'] = anchorify
        env.filters['debug'] = pprint
        template = env.get_template(self.README_TEMPLATE)
        readme = template.render(activity = self, icons_url = __icons_url__, download_url = __download_url__, Quiz = Quiz)
        # write to file
        print("generando README.md: ", readme_file)
        with open(readme_file, 'w', encoding='utf-8') as outfile:
            outfile.write(readme)

    @staticmethod    
    def create(path, force = False):
        """
        Create category descriptor
        - path: path to category
        - force: if true, overwrite existing category descriptor
        """
        descriptor = os.path.join(path, Category.METADATA_FILE)
        # check if category descriptor exists and force is false
        if os.path.isfile(descriptor) and not force:
            raise Exception(f'{path} ya es una categoría. Use --force para sobreescribir')
        # if there is category descriptor, loads it
        default_metadata = Category(path).metadata
        # create category descriptor
        category = {
            'name': input_string('Nombre', default_metadata['name']),
            'description': input_string('Descripción', default_metadata['description']),
            'category': input_list('Categoría', default_metadata['category']),
            'tags': input_list('Tags', default_metadata['tags']),
        }
        # write activity descriptor to json file
        with open(descriptor, 'w') as outfile:
            json.dump(category, outfile, indent=4)
