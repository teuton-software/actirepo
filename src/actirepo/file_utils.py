"""
File utilities.
- get_valid_filename: Returns a valid filename by removing invalid characters and replacing slashes with underscores.
- is_newer_than: Check if file1 is newer than file2
- slugify: Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated dashes to single dashes. Remove characters that aren't alphanumerics, underscores, or hyphens. Convert to lowercase. Also strip leading and trailing whitespace, dashes, and underscores.
- anchorify: Creates a valid anchor from a string: Convert to lowercase. Remove characters that aren't alphanumerics, underscores, or hyphens. Convert spaces to hyphens. Also strip leading and trailing whitespace, dashes, and underscores.
"""
import unicodedata
import re
import os


def get_valid_filename(name):
    """
    Returns a valid filename by removing invalid characters and replacing slashes with underscores.
    Args:
        name (str): The input filename.
    Returns:
        str: The valid filename.
    Raises:
        Exception: If the resulting filename is empty or contains only dots or double dots.
    """
    s = str(name).strip().replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace('"', "_").replace("<", "_").replace(">", "_").replace("|", "_").replace(" ", "_").replace("\t", "_").replace("\n", "_").replace("\r", "_").replace("\f", "_").replace("\v", "_").replace("\0", "_").replace("\b", "_").replace("\a", "_").replace("\e", "_")
    s = re.sub(r"(?u)[^- \w.]", "", s)
    if s in {"", ".", ".."}:
        raise Exception(f"Error: {name} is not a valid filename")
    return s

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
