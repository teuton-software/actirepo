import os
import json

from .artifact import Artifact
from .activity import Activity
from .category import Category

class Repo(Artifact):
    """
    Repo class
    - list_activities: list all activities in a directory
    - create_readmes: create README.md files for all activities in a directory
    - create_repo: create a repo descriptor
    - read_repo: read a repo descriptor
    """

    # repo file name
    METADATA_FILE = 'repo.json'

    def __init__(self, path):
        super().__init__(path, self.METADATA_FILE)
        self.activities = []
        self.categories = []

    def load(self):
        """
        Load repo metadata from repo.json
        """
        if self.exists():                   # check if repo exists
            # get full path to repo descriptor
            repo_file = os.path.join(self.path, self.METADATA_FILE)
            # check if repo descriptor exists
            if not os.path.isfile(repo_file):
                raise Exception(f'Error: {repo_file} no existe')
            # read repo descriptor
            with open(repo_file, 'r') as json_file:
                content = json_file.read()
            # parse repo descriptor
            repo = json.loads(content)
            # set repo metadata
            self.name = repo.get('name')
            self.description = repo.get('description')
            self.url_download = repo.get('url_download')
            self.url_pages = repo.get('url_pages')
            self.url_raw = repo.get('url_raw')
        else:
            self.description = None             # repo description
            self.url_download = None            # download base URL
            self.url_pages = None               # pages base URL
            self.url_raw = None                 # raw base URL

    def save(self):
        """
        Save repo metadata to repo.json
        """
        # get full path to repo descriptor
        repo_file = os.path.join(self.path, self.METADATA_FILE)
        # create repo descriptor
        repo = {
            'name': self.name,
            'description': self.description,
            'url_download': self.url_download,
            'url_pages': self.url_pages,
            'url_raw': self.url_raw
        }
        # write repo descriptor
        with open(repo_file, 'w') as json_file:
            json.dump(repo, json_file, indent=4)

    def __str__(self):
        return f'Repo {self.name} ({len(self.activities)} activities, {len(self.categories)} categories)'

    def list(self):
        """
        List all activities in a directory recursively
        """
        if not os.path.isdir(self.path):
            raise Exception(f'Error: {self.path} no es un directorio')
        content = {
            'activities': [],
            'categories': []
        }
        # walk throuth all directories
        for root, dirs, files in os.walk(self.path):
            # check if is an activity
            if Activity.is_activity(root):
                # get metadata
                activity = Activity(root)
                content['activities'].append(activity)
            if Category.is_category(root):
                # get metadata
                category = Category(root, True)            
                content['categories'].append(category)
        return content

    @staticmethod
    def is_repo(path):
        """
        Check if a directory is a repo
        - path: directory path
        - return: True if is a repo, False otherwise
        """
        return os.path.isfile(os.path.join(path, Repo.METADATA_FILE))
    
    @staticmethod
    def read(path):
        """
        Read a repo descriptor
        """
        # get full path to repo descriptor
        repo_file = os.path.join(path, Repo.METADATA_FILE)
        # read repo descriptor
        with open(repo_file, 'r') as json_file:
            content = json_file.read()
        # parse repo descriptor
        return json.loads(content)

    def create_readme_repo(path, force):
        """
        Create a README.md file for a repo
        - path: directory path
        - force: overwrite existing README.md file
        """
        # get full path to README.md file
        readme_file = os.path.join(path, 'README.md')
        # check if README.md file exists
        if not os.path.isfile(readme_file) or force:
            # get repo metadata
            repo = Repo.read(path)
            # create README.md content
            content = f'# {os.path.basename(path)}\n\n'
            content += f'## Actividades\n\n'
            for activity in repo['activities']:
                content += f'- [{activity["name"]}](./{activity["path"]})\n'
            # write README.md file
            with open(readme_file, 'w') as file:
                file.write(content)

    def create_readmes(self, path, recursive, force):
        """
        Create README.md files for all activities in a directory
        - path: directory path
        - recursive: create README.md files recursively
        - force: overwrite existing README.md files
        """
        print(f'Creando README.md en "{path}"...')
        if Activity.is_activity(path):
            activity = Activity(path)
            activity.create_readme(activity, force)
        elif Repo.is_repo(path):
            self.create_readme_repo(path, force)
        if recursive:
            for dir in os.listdir(path):
                subdir = os.path.join(path, dir)
                if os.path.isdir(subdir):
                    self.create_readmes(subdir, recursive, force)

    def create_repo(self, repo_path, force=False):
        """
        Create a repo descriptor
        - repo_path: directory path
        - return: repo descriptor
        """
        # check if path exsists
        if not os.path.isdir(repo_path):
            raise Exception(f'Error: {repo_path} no es un directorio')
        # get full path to activity descriptor
        repo_file = os.path.join(repo_path, self.__filename)
        # check if repo file exists
        if os.path.isfile(repo_file) and not force:
            raise Exception(f'Error: {repo_file} ya existe')
        # get all activities in repo
        activities = self.list_activities(repo_path)
        # create repo descriptor
        repo = {
            "activities": activities
        }
        # write repo descriptor
        with open(repo_file, 'w') as json_file:
            json.dump(repo, json_file, indent=4)


    # create_index("..")