"""
Functions for rendering html to images and getting the size of the html
"""

import contextlib
import os
import tempfile
import io
import base64

from html2image import Html2Image
from PIL import Image

# flags used to launch Chrome (custom_flags replaces html2image defaults, so they are included here)
CHROME_FLAGS = [
    "--hide-scrollbars",
    "--default-background-color=00000000"
]

def configure(no_sandbox = False):
    """
    Configure how Chrome is launched to render html
    - no_sandbox: if true, launch Chrome without sandbox (needed in some CI/Docker environments)
    """
    if no_sandbox and "--no-sandbox" not in CHROME_FLAGS:
        CHROME_FLAGS.append("--no-sandbox")

def html2png(html, destination_dir, img_file):
    """
    Render html to png image
    - html: html string
    - destination_dir: destination directory
    - img_file: image file name
    """
    hti = Html2Image(custom_flags=CHROME_FLAGS)
    hti.output_path = destination_dir
    with open(os.devnull, 'w') as devnull, contextlib.redirect_stdout(devnull):
        img_file = hti.screenshot(html_str=html, save_as=img_file)[0]
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

def get_image_size(file):
    """
    Get image size from file
    file: file element
    return { "width": int, "height": int }
    """
    if not file:
        return None
    with Image.open(io.BytesIO(base64.decodebytes(bytes(file.text, "utf-8")))) as img:
        size = img.size
        return {
            "width": size[0],
            "height": size[1]
        }
