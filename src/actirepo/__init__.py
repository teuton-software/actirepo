import json
from importlib import resources

try:
    import tomllib
except ModuleNotFoundError:
    # Third party imports
    import tomli as tomllib

# Read URL of the Real Python feed from config file
_cfg = tomllib.loads(resources.read_text("actirepo", "config.toml"))

# repo descriptor file
REPO_FILE = 'repo.json'

try:
    # read repo descriptor
    with open(REPO_FILE, 'r') as json_file:
        content = json_file.read()
    # parse repo descriptor
    repo = json.loads(content)
except Exception as e:
    # valores por defecto
    repo = {
        "download_url": "https://github.com/<profile>",
        "raw_url": "https://raw.githubusercontent.com/<profile>",
        "pages_url": "https://<profile>.github.io"
    }

# init global variables
__version__ = "0.0.1"
__raw_url__ = repo['raw_url']
__download_url__ = repo['download_url']
__pages_url__ = repo['pages_url']
__icons_url__ = _cfg["config"]["icons_url"]
