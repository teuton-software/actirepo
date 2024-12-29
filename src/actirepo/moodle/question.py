import os

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from abc import ABC

from actirepo import __icons_url__
from actirepo.utils.mime_utils import get_mimetype
from actirepo.utils.url_utils import encode
from actirepo.utils.file_utils import get_available_filename, slugify
from actirepo.utils.image_utils import html2png

TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')

class Question(ABC):

    def __init__(self, element):
        self.element = element
        self.type = self.element.get('type')
        self.name = self.element.find('name').find('text').text
        self.statement = self.__process_text(self.element.find('questiontext'))
        self.answers = [ answer.text for answer in element.findall('answer') ]
        self.image_filename = None

    def __process_text(self, element):
        """
        Process text in question element
        - element: question element
        - return: html with embedded attachments
        """
        attachments = [ 
            {
                "name": file.get('name'),
                "path": file.get('path'),
                "type": get_mimetype(file.get('name')),
                "image": f"data:{get_mimetype(file.get('name'))};{file.get('encoding')},{file.text}"
            } for file in element.findall('file')    
        ]
        html = BeautifulSoup(element.find('text').text, 'html.parser')
        for attachment in attachments:
            for img in html.find_all('img'):
                if f"@@PLUGINFILE@@{attachment.get('path')}{encode(attachment.get('name'))}" in img.get('src'):
                    img['class'] = img.get('class', []) + ['img-fluid']
                    img['src'] = attachment.get('image')
        return html.prettify()

    def render(self, destination_dir, save_html = False):
        """
        Render question as image
        - question: question xml element
        - destination_dir: directory to save question image
        - save_html: also save html to file
        - return: image filename
        """
        # create question data
        print(f"generando imagen {self.type} para la pregunta ", self.name)
            
        # render html from template
        env = Environment(loader = FileSystemLoader(TEMPLATES_PATH, encoding='utf8'))
        template = env.get_template(f'{self.type}.template.html')
        html = template.render(question = self, icons_url = __icons_url__)

        # html to image
        self.image_filename = get_available_filename(destination_dir, slugify(self.name) + ".png")
        html2png(html, destination_dir, self.image_filename)

        # writes html to file
        if save_html:
            html_filename = self.image_filename.replace('.png', '.html')
            with open(os.path.join(destination_dir, html_filename), 'w') as outfile:
                outfile.write(html)
        
        return self.image_filename
        
    def __str__(self):
        return f"{self.type}: {self.name}"
