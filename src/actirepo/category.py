import os
import json

from jinja2 import Environment, FileSystemLoader
from pprint import pprint

from .__init__ import __icons_url__
from .utils.file_utils import is_newer_than, anchorify, path_to_capitalized_list
from .utils.console import title, input_string, input_list
from .artifact import Artifact
from .activity import Activity
from .moodle.quiz import Quiz
from .moodle.stats import Stats

class Category(Artifact):
    """
    Category class: represents a category of activities
    """

    # category README template
    README_TEMPLATE = 'README.category.template.md'

    # metadata filename
    METADATA_FILE = 'category.json'

    def __init__(self, path):
        super().__init__("category", path, self.METADATA_FILE)

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
            with open(self.descriptor, 'r', encoding = 'utf-8') as json_file:
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
        self.metadata['stats'] = self.get_stats()
        return self.metadata

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

    def create_readme(self, recursive = False):
        """
        Create README.md file for category (including all activities in category and subcategories)
        - recursive: if true, create README.md files recursively
        """
        # print message
        title(f'Creating README.md for {self.type} in {self.path}...')
        # if recursive, create README.md file for subcategories
        if recursive:
            for actitivy in self.activities:
                actitivy.create_readme(True)
            for subcategory in self.categories:
                subcategory.create_readme(recursive)
        # load and render template
        env = Environment(loader = FileSystemLoader(self.TEMPLATES_PATH, encoding='utf8'))
        env.filters['anchorify'] = anchorify
        env.filters['debug'] = pprint
        env.filters['difficulty_to_string'] = Activity.difficulty_to_string
        env.filters['difficulty_to_minibadge'] = Activity.difficulty_to_minibadge
        template = env.get_template(self.README_TEMPLATE)
        readme = template.render(category = self, icons_url = __icons_url__, Quiz = Quiz)
        # write to file
        with open(self.readme_file, 'w', encoding='utf-8') as outfile:
            outfile.write(readme)

    @staticmethod    
    def create(path):
        """
        Create category descriptor
        - path: path to category
        """
        descriptor = os.path.join(path, Category.METADATA_FILE)
        # if there is category descriptor, loads it
        default_metadata = Category(path).metadata
        # create category descriptor
        category = {
            'name': input_string('Name', default_metadata['name']),
            'description': input_string('Description', default_metadata['description']),
            'category': input_list('Category', default_metadata['category']),
            'tags': input_list('Tags', default_metadata['tags']),
        }
        # write category descriptor to json file
        with open(descriptor, 'w', encoding = 'utf-8') as outfile:
            json.dump(category, outfile, indent=4)
