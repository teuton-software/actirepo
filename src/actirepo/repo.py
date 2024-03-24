"""
Repo module
- list_activities: list all activities in a directory
- create_readmes: create README.md files for all activities in a directory
- create_repo: create a repo descriptor
- read_repo: read a repo descriptor
"""

import os
import json

from actirepo.activity import is_activity, read_activity, create_readme_activity

# repo file name
REPO_FILE = 'repo.json'

def list_activities(repo_path="."):
    """
    List all activities in a directory recursively
    - repo_path: directory path
    - return: list of activities
    """
    if not os.path.isdir(repo_path):
        raise Exception(f'Error: {repo_path} no es un directorio')
    activities = []
    # walk throuth all directories
    for root, dirs, files in os.walk(repo_path):
        # check if is an activity
        if is_activity(root):
            # get metadata
            metadata = read_activity(root, True)            
            activities.append(metadata)
    return activities

def is_repo(path):
    """
    Check if a directory is a repo
    - path: directory path
    - return: True if is a repo, False otherwise
    """
    return os.path.isfile(os.path.join(path, REPO_FILE))

def create_readme_repo(path, force):
    """
    Create a README.md file for a repo
    - path: directory path
    - force: overwrite existing README.md file
    """
    # get full path to README.md file
    readme_file = os.path.join(path, 'README.md')
    # check if README.md file exists
    if os.path.isfile(readme_file) and not force:
        raise Exception(f'Error: {readme_file} ya existe')
    # get repo metadata
    repo = read_repo(path)
    # create README.md content
    content = f'# {os.path.basename(path)}\n\n'
    content += f'## Actividades\n\n'
    for activity in repo['activities']:
        content += f'- [{activity["name"]}](./{activity["path"]})\n'
    # write README.md file
    with open(readme_file, 'w') as file:
        file.write(content)

def create_readmes(path, recursive, force):
    """
    Create README.md files for all activities in a directory
    - path: directory path
    - recursive: create README.md files recursively
    - force: overwrite existing README.md files
    """
    if is_activity(path):
        activity = read_activity(path)
        create_readme_activity(activity, force)
    if is_repo(path):
        create_readme_repo(path, force)
    if recursive:
        for dir in os.listdir(path):
            subdir = os.path.join(path, dir)
            if os.path.isdir(subdir):
                create_readmes(subdir, recursive, force)

def create_repo(repo_path):
    """
    Create a repo descriptor
    - repo_path: directory path
    - return: repo descriptor
    """
    # check if path exsists
    if not os.path.isdir(repo_path):
        raise Exception(f'Error: {repo_path} no es un directorio')
    # get full path to activity descriptor
    repo_file = os.path.join(repo_path, REPO_FILE)
    # check if repo file exists
    if os.path.isfile(repo_file):
        raise Exception(f'Error: {repo_file} ya existe')
    # get all activities in repo
    activities = list_activities(repo_path)
    # create repo descriptor
    repo = {
        "activities": activities
    }
    # write repo descriptor
    with open(repo_file, 'w') as json_file:
        json.dump(repo, json_file, indent=4)

# read repo metadata
def read_repo(repo_path):
    # get full path to activity descriptor
    repo_file = os.path.join(repo_path, REPO_FILE)
    # read activity descriptor
    with open(repo_file, 'r') as json_file:
        content = json_file.read()
    # parse activity descriptor
    return json.loads(content)

# create_index("..")