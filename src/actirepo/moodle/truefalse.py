from .question import Question

class TrueFalse(Question):

    def __init__(self, element):
        super().__init__(element)
        self.answers = [
            {
                "text": answer.find('text').text,
                "feedback": answer.find('feedback').find('text').text,
                "fraction": float(answer.get('fraction'))
            } for answer in self.element.findall('answer')
        ]