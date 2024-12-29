import os

from actirepo.artifact import Artifact

class Category(Artifact):

    METADATA_FILE = 'category.json'

    def __init__(self, path):
        super().__init__(path, self.METADATA_FILE)
        self.activities = []
        self.categories = []

    @staticmethod
    def path_to_categories(path):
        """
        Convert path to a chain of categories
        - path: path to convert to categories
        - returns: list of categories
        """
        parts = path.split(os.sep)
        return [ part.capitalize() for part in parts[0:len(parts)-1] ]
    
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
    def __just_contains_folders(self, path):
        """
        Check if a path just contains folders
        """
        for dirs in os.listdir(path):
            if not os.path.isdir(dirs):
                return False
        return True                

    def __str__(self):
        return f'Category {self.name}'