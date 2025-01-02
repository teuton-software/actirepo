"""
File utilities.
- get_available_filename: Get valid filename
- is_newer_than: Check if file1 is newer than file2
- slugify: Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated dashes to single dashes. Remove characters that aren't alphanumerics, underscores, or hyphens. Convert to lowercase. Also strip leading and trailing whitespace, dashes, and underscores.
- anchorify: Creates a valid anchor from a string: Convert to lowercase. Remove characters that aren't alphanumerics, underscores, or hyphens. Convert spaces to hyphens. Also strip leading and trailing whitespace, dashes, and underscores.
"""
import unicodedata
import re
import os
from pathlib import Path

def remove_extension(filename):
    """
    Remove extension from filename
    - filename: filename to remove extension
    - return: filename without extension
    """
    return Path(filename).stem


def get_available_filename(path, name):
    """
    Get the first available filename, searching for a valid and not existing filename by appending an index to the name.
    - path: path to directory
    - name: name of the file
    - return: first available filename
    """
    index = 1
    basename = os.path.splitext(name)[0]
    extension = os.path.splitext(name)[1][1:] # get extension without dot
    valid_filename = f'{basename}_{index}.{extension}'
    while os.path.exists(os.path.join(path, valid_filename)):
        index += 1
        valid_filename = f'{basename}_{index}.{extension}'
    return valid_filename

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def anchorify(value):
    """
    Creates a valid anchor from a string:
    - Convert to lowercase. 
    - Remove characters that aren't alphanumerics, underscores, or hyphens. 
    - Convert spaces to hyphens. 
    - Also strip leading and trailing whitespace, dashes, and underscores.
    """
    return re.sub(r'[^\w\s-]', '', value.lower()).replace(" ", "-")

def is_newer_than(tested_file, files):
    """
    Check if file is newer than all files
    Returns True if file is newer than all files; False otherwise.
    """
    for file in files:
        if not os.path.isfile(file):
            continue
        if os.path.getmtime(tested_file) < os.path.getmtime(file):
            return False
    return True

def path_to_capitalized_list(path):
    """
    Convert path to a list
    - path: path to convert
    - returns: list of parts of the path
    """
    parts = path.split(os.sep)
    return [ part.capitalize() for part in parts[0:len(parts)-1] ]
