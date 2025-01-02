import os
import json

from actirepo.utils.console import input_string
from actirepo.category import Category

class Repo(Category):
    """
    Repo class: represents a repository of activities
    """

    # repository README template
    README_TEMPLATE = 'README.repo.template.md'

    # repo file name
    METADATA_FILE = 'repo.json'

    def __init__(self, path):
        super().__init__(path)
        self.type = "repository"

    @staticmethod
    def create(path):
        """
        Create repository descriptor
        - path: path to repository
        """
        descriptor = os.path.join(path, Repo.METADATA_FILE)
        # if there is repository descriptor, loads it
        default_metadata = Repo(path).metadata
        # create category descriptor
        category = {
            'name': input_string('Name', default_metadata['name']),
            'description': input_string('Description', default_metadata['description']),
        }
        # write repository descriptor to json file
        with open(descriptor, 'w', encoding = 'utf-8') as outfile:
            json.dump(category, outfile, indent=4)
