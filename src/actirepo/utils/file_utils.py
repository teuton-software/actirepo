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

def is_newer_than(file1, file2):
    """
    Check if file1 is newer than file2
    Returns True if file1 is a file and file2 is a file and file1 is newer than file2.
    """
    return os.path.isfile(file1) and os.path.getmtime(file2) < os.path.getmtime(file1)

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
