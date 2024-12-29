import os
import mimetypes

mimetypes.init()

def get_mimetype(filename):
    """
    Get mimetype from file
    - filename: file name with extension
    - return: mimetype string
    """
    if not filename:
        return None
    return mimetypes.types_map[os.path.splitext(filename)[1]]