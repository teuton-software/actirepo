
from .question import Question

class MultiChoice(Question):

    def __init__(self, element):
        super().__init__(element)
        self.answers = [
            {
                "text": answer.find('text').text.replace('<p>', '<p style="margin:0px 0px 7.5px;margin-top:0px;margin-bottom:7.5px;box-sizing:border-box;">'),
                "feedback": answer.find('feedback').find('text').text,
                "fraction": float(answer.get('fraction')),
                "letter": chr(65 + i).lower()
            } for i, answer in enumerate(element.findall('answer'))
        ]
        self.single = len([ answer for answer in element.findall('answer') if float(answer.get('fraction')) > 0 ]) == 1