"""
Functions for rendering html to images and getting the size of the html
"""

import contextlib
import os
import tempfile
from html2image import Html2Image
from PIL import Image

def html2png(html, destination_dir, img_file):
    """
    Render html to png image
    - html: html string
    - destination_dir: destination directory
    - img_file: image file name
    """
    hti = Html2Image()
    hti.output_path = destination_dir
    with open(os.devnull, 'w') as devnull:
        with contextlib.redirect_stdout(devnull):
                hti.screenshot(html_str=html, save_as=img_file)
    img_file = os.path.join(destination_dir, img_file)
    im = Image.open(img_file)
    im = im.crop(im.getbbox())
    im.save(img_file)

def htmlsize(html):
    """
    Get the size of the html
    - html: html string
    - return: dictionary with width and height {"width": width, "height": height}
    """
    tmp = tempfile.mkstemp(suffix='.png')
    os.close(tmp[0])
    file = tmp[1]
    html2png(html, os.path.dirname(file), os.path.basename(file))
    im = Image.open(file)
    size = im.size
    im.close()
    os.remove(file)
    return {
        "width": size[0],
        "height": size[1]
    }

