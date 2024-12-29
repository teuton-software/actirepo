import json
from importlib import resources
from pprint import pprint

# check if tomllib is installed
try:
    import tomllib
except ModuleNotFoundError:
    # third party import
    import tomli as tomllib

# read config from file
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
        "url_download": "https://github.com/teuton-software",
        "url_raw": "https://raw.githubusercontent.com/teuton-software",
        "url_pages": "https://<profile>.github.io"
    }

# init global variables
__module__ = 'actirepo'
__version__ = '0.0.1'
__raw_url__ = repo['url_raw']
__download_url__ = repo['url_download']
__pages_url__ = repo['url_pages']
__icons_url__ = _cfg["config"]["icons_url"]
