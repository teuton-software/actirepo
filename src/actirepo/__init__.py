from pathlib import Path
import tomllib

# read pyproject.toml from the root directory
root_dir = Path(__file__).resolve().parent.parent.parent
pyproject_path = root_dir / "pyproject.toml"
with pyproject_path.open("rb") as f:
    _pyp = tomllib.load(f)

# init global variables
__module__ = 'actirepo'
__icons_url__ = "https://raw.githubusercontent.com/teuton-software/actirepo/master/icons"
__project_name__ = _pyp["project"]["name"]
__project_version__ = _pyp["project"]["version"]
__project_description__ = _pyp["project"]["description"]
__project_url__ = _pyp["project"]["urls"]["Homepage"]