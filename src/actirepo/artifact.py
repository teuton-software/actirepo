from abc import ABC, abstractmethod
import os

class Artifact(ABC):

    # get module path
    MODULE_PATH = os.path.dirname(os.path.realpath(__file__))

    # load and render template
    TEMPLATES_PATH = os.path.join(MODULE_PATH, 'templates')

    def __init__(self, path, filename) -> None:
        print("initializing artifact...")
        path = os.path.normpath(path)
        self.path = path
        self.name = os.path.basename(path)
        self.filename = filename
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


