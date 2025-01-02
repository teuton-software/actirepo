from abc import ABC, abstractmethod
import json
import os

class Artifact(ABC):

    # default README file
    README = 'README.md'

    # get module path
    MODULE_PATH = os.path.dirname(os.path.realpath(__file__))

    # load and render template
    TEMPLATES_PATH = os.path.join(MODULE_PATH, 'templates')

    def __init__(self, type, path, filename) -> None:
        print(f"Initializing {type}: {path}...")
        if (not os.path.exists(path)):
            raise FileNotFoundError(f"Path {path} does not exist.")
        self.type = type
        self.path = os.path.normpath(path)
        self.name = os.path.basename(self.path)
        self.filename = filename
        self.readme_file = os.path.join(self.path, Artifact.README)
        self.descriptor = os.path.join(self.path, filename)
        self.metadata = self.load()

    def __str__(self) -> str:
        return f'{self.name}'
    
    __repr__ = __str__
    
    def exists(self) -> bool:
        return os.path.exists(self.path)

    @abstractmethod
    def load(self) -> dict:
        pass

    def save(self):
        """
        Save activity descriptor
        """
        with open(self.descriptor, 'w') as outfile:
            json.dump(self.metadata, outfile, indent=4)


