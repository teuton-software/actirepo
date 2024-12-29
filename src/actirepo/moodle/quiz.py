"""
Quiz 
- render_question: render question as image
"""

import os
import shutil
import xml.etree.ElementTree as ET

from actirepo.__init__ import __icons_url__, __download_url__

from actirepo.utils.url_utils import normalize
from actirepo.utils.file_utils import anchorify

from actirepo.moodle.shortanswer import ShortAnswer
from actirepo.moodle.multichoice import MultiChoice
from actirepo.moodle.truefalse import TrueFalse
from actirepo.moodle.ddimageortext import DDImageOrText
from actirepo.moodle.ddmarker import DDMarker
from actirepo.moodle.essay import Essay

class Quiz():
    """
    Quiz: class to manage quiz files
    """

     # supported question types
    SUPPORTED_QUESTIONS = {
        'shortanswer': {
            'class': ShortAnswer,
            'description': 'Respuesta corta'
        },
        'multichoice': {
            'class': MultiChoice,
            'description': 'Selección múltiple'
        },
        'truefalse':{ 
            'class': TrueFalse,
            'description': 'Verdadero/Falso'
        },
        'ddimageortext': {
            'class': DDImageOrText,
            'description': 'Arrastrar y soltar imagen o texto'
        },
        'ddmarker': {
            'class': DDMarker,
            'description': 'Arrastrar y soltar marcador'
        },       
        'essay': {
            'class': Essay,
            'description': 'Ensayo'
        },
        #'numerical': {
        #    'class', Numeric,
        #    'description': 'Numérico'
        #},
        #'matching': {
        #    'class': Matching,
        #    'description': 'Emparejamiento'
        #},
        #'cloze': {
        #    'class': Cloze,
        #    'description': 'Asociar'
        #}
    }

    # anchorified question types
    #ANCHORIFIED_SUPPORTED_QUESTIONS = { key : anchorify(value) for key, value in SUPPORTED_QUESTIONS.items() }

    def __init__(self, quizfile):
        if not Quiz.is_quiz_file(quizfile):
            raise Exception(f'Error: {quizfile} is not a quiz file')
        self.quizfile = quizfile
        self.filename = os.path.basename(quizfile)
        self.path = os.path.dirname(quizfile)
        self.root = ET.parse(quizfile).getroot()
        self.questions = self.__read_questions()

    def __read_questions(self):
        """
        Get questions from file
        - activity_path: path to activity
        - file: questions file
        - returns: list of questions organized by file and type
        """
        # search "question" tags under "quiz" tag
        questions = {}
        for element in self.root.findall('question'):
            # get question type
            type = element.get('type')
            # skip if question type is not supported
            if not type in self.SUPPORTED_QUESTIONS.keys():
                continue
            # create question
            question = self.SUPPORTED_QUESTIONS[type]['class'](element)
            # check if question type is in types dictionary, and add it if not
            if not type in questions:
                questions[type] = [ question ]
            else:
                questions[type].append(question)
        # return questions organized by type
        return questions
    
    def get_types(self):
        """
        Get question types
        """
        return { type for type in self.questions }

    def get_stats(self):
        return {
            'types': { type: len(question) for type, question in self.questions.items() },
            'total': sum([len(question) for question in self.questions.values()])
        }

    def generate_images(self, limit=9999, force=True):
        """
        Generate images for questions in activity
        - activity: activity descriptor
        - force: if true, overwrite existing images
        """
        images_dir = os.path.join(self.path, "images")
        # if images directory exists and force is true, delete it
        if os.path.isdir(images_dir) and force:
            print("Overwriting existing images...")
            shutil.rmtree(images_dir)
        # create images dictionary
        images = {}
        # walk through all questions in file
        for type, questions in self.questions.items():
            count = 0
            # walk through all questions of the same type
            for question in questions:
                # render image for question
                image_file = question.render(images_dir)
                # if image was generated, add it to dictionary
                if image_file:
                    count += 1
                    # check if question type is in images dictionary, and add it if not
                    if not type in images:
                        images[type] = [ image_file ]
                    else:
                        images[type].append(image_file)
                if count >= limit:
                    break        
        return images

    @staticmethod
    def is_quiz_file(quiz_file):
        """
        Check if a file is a quiz file
        - questions_file: path to questions file
        - returns: True if file is a quiz file, False otherwise
        """
        # check if file is an xml file
        if not quiz_file.endswith('.xml'):
            return False
        # get full path to questions file and parse xml
        try:
            tree = ET.parse(quiz_file)
            # check if root is "quiz" tag 
            return tree.getroot().tag == 'quiz'
        except:
            return False

    def __str__(self):
        return f'{self.quizfile}'
    
    __repr__ = __str__
