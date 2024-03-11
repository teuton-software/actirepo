import os
import json

from actirepo.activity import is_activity, read_activity, create_readme

REPO_FILE = 'repo.json'

def list_activities(repo_path="."):
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

# create README.md files for all activities in path
def create_readmes(path, recursive, force):
    if is_activity(path):
        activity = read_activity(path)
        create_readme(activity, force)
    for dir in os.listdir(path):
        subdir = os.path.join(path, dir)
        if os.path.isdir(subdir):
            create_readmes(subdir, recursive, force)

def create_index(repo_path="."):
    # check if path exsists
    if not os.path.isdir(repo_path):
        raise Exception(f'Error: {repo_path} no es un directorio')    
    acitivies_list = []
    # walk throuth all directories
    for root, dirs, files in os.walk(repo_path):
        # check if is an activity
        if is_activity(root):
            # get metadata
            metadata = read_activity(root)
            # total = get_num_questions(root)
            activity = {
                "name": metadata['name'],
                "description": metadata['description'],
                # "total": total,
            }
            acitivies_list.append(activity)
    print(acitivies_list)

def create_repo(repo_path=""):
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