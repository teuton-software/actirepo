from abc import ABC, abstractmethod
import os

class Artifact(ABC):

    # default README file
    README = 'README.md'

    # get module path
    MODULE_PATH = os.path.dirname(os.path.realpath(__file__))

    # load and render template
    TEMPLATES_PATH = os.path.join(MODULE_PATH, 'templates')

    def __init__(self, path, filename) -> None:
        print(f"Initializing artifact {path}...")
        if (not os.path.exists(path)):
            raise FileNotFoundError(f"Path {path} does not exist.")
        path = os.path.normpath(path)
        self.path = path
        self.name = os.path.basename(path)
        self.filename = filename
        self.readme_file = os.path.join(path, Artifact.README)
        self.descriptor = os.path.join(path, filename)
        self.metadata = self.load()

    def __str__(self) -> str:
        return f'{self.name}'
    
    __repr__ = __str__
    
    def exists(self) -> bool:
        return os.path.exists(self.path)

    @abstractmethod
    def create_readme(self) -> str:
        pass
    
    @abstractmethod
    def load(self) -> dict:
        pass

    @abstractmethod
    def save(self) -> None:
        pass


