import os
import xml.etree.ElementTree as ET
import mimetypes
import io
import base64

from actirepo.__init__ import __icons_url__, __download_url__
from actirepo.url_utils import encode
from actirepo.image_utils import html2png, htmlsize
from actirepo.file_utils import slugify
from actirepo.console import format_bytes

from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup
from PIL import Image

def _get_mimetype(file):
    """
    Get mimetype from file
    - file: file element
    - return: mimetype string
    """
    if not file:
        return None
    return mimetypes.types_map[os.path.splitext(file.get('name'))[1]]

def _get_image_size(file):
    """
    Get image size from file
    file: file element
    return { "width": int, "height": int }
    """
    print("hay file")
    if not file:
        return None
    with Image.open(io.BytesIO(base64.decodebytes(bytes(file.text, "utf-8")))) as img:
        size = img.size
        return {
            "width": size[0],
            "height": size[1]
        }
    
def _get_valid_image_filename(path, name, index = 1):
    """
    Get valid image filename
    - path: path to directory
    - name: name of the file
    - index: index to append to name
    - return: valid filename
    """
    valid_name = slugify(name) + f'_{index}'
    if not os.path.exists(os.path.join(path, f'{valid_name}.png')):
        return f'{valid_name}.png'
    return _get_valid_image_filename(path, name, index + 1)    

def _process_attachments(element):
    """
    Process attachments in question element
    - element: question element
    - return: html with attachments
    """
    attachments = [ 
        {
            "name": file.get('name'),
            "path": file.get('path'),
            "type": _get_mimetype(file),
            "image": f"data:{_get_mimetype(file)};{file.get('encoding')},{file.text}"
        } for file in element.findall('file')
    ]
    html = BeautifulSoup(element.find('text').text, 'html.parser')
    for attachment in attachments:
        for img in html.find_all('img'):
            if f"@@PLUGINFILE@@{attachment.get('path')}{encode(attachment.get('name'))}" in img.get('src'):
                img['class'] = img.get('class', []) + ['img-fluid']
                img['src'] = attachment.get('image')
    return html.prettify()

# get size of text
def _drop_text_size(text):
    """
    Get size of html text element
    - text: text element
    - return: { "width": int, "height": int }
    """
    html = f"""
    <div style="box-sizing:border-box;">
        <div style="padding: 5px;box-sizing:border-box;background-color:rgb(220, 220, 220);border-radius:0px 10px 0px 0px;display:none;vertical-align:top;margin:5px;height: auto;width: auto;cursor:move;border:1px solid rgb(0, 0, 0);font:13px / 16.003px arial, helvetica, clean, sans-serif;">{text}</div>
        <div style="padding: 5px;user-select:none;box-sizing:border-box;background-color:rgb(220, 220, 220);border-radius:0px 10px 0px 0px;vertical-align:top;margin:5px;height: auto;width: auto;cursor:move;border:1px solid rgb(0, 0, 0);display:inline-block;font:13px / 16.003px arial, helvetica, clean, sans-serif;">{text}</div>
    </div>
    """
    return htmlsize(html)

def render_question(question, destination_dir, save_html = False):
    """
    Render question as image
    - question: question xml element
    - destination_dir: directory to save question image
    - save_html: also save html to file
    - return: image filename
    """
    type = question.get("type")
    # create question data
    question_data = {
        "type": question.get('type'),
        "name": question.find('name').find('text').text,
        "statement": _process_attachments(question.find('questiontext'))
    }
    print(f"generando imagen {question_data.get("type")}: ", question_data.get("name"))
    # check question type
    match type:
        case "truefalse":
            question_data.update(
                { 
                    "answers": [
                        {
                            "text": answer.find('text').text,
                            "feedback": answer.find('feedback').find('text').text,
                            "fraction": float(answer.get('fraction'))
                        } for answer in question.findall('answer')
                    ]
                }
            )
        case "shortanswer":
            question_data.update(
                { 
                    "answers": [
                        {
                            "text": answer.find('text').text,
                            "feedback": answer.find('feedback').find('text').text,
                            "fraction": float(answer.get('fraction'))
                        } for answer in question.findall('answer')
                    ],
                    "first_answer": question.findall('answer')[0].find('text').text
                }
            )
        case "multichoice":
            question_data.update(
                { 
                    "answers": [
                        {
                            "text": answer.find('text').text.replace('<p>', '<p style="margin:0px 0px 7.5px;margin-top:0px;margin-bottom:7.5px;box-sizing:border-box;">'),
                            "feedback": answer.find('feedback').find('text').text,
                            "fraction": float(answer.get('fraction')),
                            "letter": chr(65 + i).lower()
                        } for i, answer in enumerate(question.findall('answer'))
                    ],
                    "single": len([ answer for answer in question.findall('answer') if float(answer.get('fraction')) > 0 ]) == 1
                }
            )
        case "ddmarker":
            background_file = question.find('file')
            question_data.update(
                { 
                    "drags": [
                        {
                            "no": int(drag.find('no').text),
                            "text": drag.find('text').text
                        } for drag in question.findall('drag')
                    ],              
                    "background": f"data:{_get_mimetype(background_file)};{background_file.get('encoding')},{background_file.text}",
                }
            )
        case "ddimageortext":
            background_file = question.find('file')
            question_data.update(
                { 
                    "background": f"data:{_get_mimetype(background_file)};{background_file.get('encoding')},{background_file.text}",
                    "drags": {
                        int(drag.find('no').text) : {
                            "no": int(drag.find('no').text),
                            "text": drag.find('text').text,
                            "type": "text" if drag.find('file') is None else "image",
                            "image": f"data:{_get_mimetype(drag.find('file'))};{drag.find('file').get('encoding')},{drag.find('file').text}" if drag.find('file') is not None else None,
                            "size": _drop_text_size(drag.find('text').text) if not drag.find('file') else _get_image_size(drag.find('file')),
                            "draggroup": int(drag.find('draggroup').text)
                        } for drag in question.findall('drag')
                    },
                    "drops": {
                        int(drop.find('choice').text) : {
                            "no": int(drop.find('no').text),
                            "text": drop.find('text').text,
                            "choice": int(drop.find('choice').text),
                            "xleft": int(drop.find('xleft').text),
                            "ytop": int(drop.find('ytop').text)
                        } for drop in question.findall('drop')
                    }
                }
            )
            # add drag sizes to drops
            for choice, drop in question_data['drops'].items():
                drop['size'] = question_data['drags'][choice]['size']
            # group drags by draggroup
            question_data['draggroups'] = {}
            for drag in question_data['drags'].values():
                if not drag['draggroup'] in question_data['draggroups']:
                    question_data['draggroups'][drag['draggroup']] = [ drag['no'] ]
                else:
                    question_data['draggroups'][drag['draggroup']].append(drag['no'])
            # get max width and height for each draggroup
            question_data['draggroups_size'] = {}
            for draggroup, drags in question_data['draggroups'].items():
                max_width = 0
                max_height = 0
                for drag_no in drags:
                    drag_size = question_data['drags'][drag_no]['size']
                    if drag_size['width'] > max_width:
                        max_width = drag_size['width']
                    if drag_size['height'] > max_height:
                        max_height = drag_size['height']
                question_data['draggroups_size'][draggroup] = {
                    "width": max_width,
                    "height": max_height
                }
        case "essay":
            question_data.update(
                { 
                    "editor": question.find('responseformat').text != 'noinline',
                    "response_lines": int(question.find('responsefieldlines').text),
                    "file_upload": int(question.find('attachments').text) > 0,
                    "max_size": format_bytes(int(question.find('maxbytes').text)) if int(question.find('maxbytes').text) > 0 else "Por defecto",
                    "max_files": int(question.find('attachments').text),
                    "file_types": question.find('filetypeslist').text.split(',') if not question.find('filetypeslist').text is None else []
                }
            )
        case _:
            return
        
    # render html from template
    templates_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
    env = Environment(loader = FileSystemLoader(templates_path, encoding='utf8'))
    template = env.get_template(f'{question_data['type']}.template.html')
    html = template.render(question = question_data, icons_url = __icons_url__)

    # html to image
    image_filename = _get_valid_image_filename(destination_dir, question_data['name'])
    html2png(html, destination_dir, image_filename)

    # writes html to file
    if save_html:
        html_filename = image_filename.replace('.png', '.html')
        with open(os.path.join(destination_dir, html_filename), 'w') as outfile:
            outfile.write(html)
    
    return image_filename

mimetypes.init()
