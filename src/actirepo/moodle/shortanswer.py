from .question import Question

class ShortAnswer(Question):

    def __init__(self, element):
        super().__init__(element)
        self.answers = [
            {
                "text": answer.find('text').text,
                "feedback": answer.find('feedback').find('text').text,
                "fraction": float(answer.get('fraction'))
            } for answer in element.findall('answer')
        ]
        self.first_answer = element.findall('answer')[0].find('text').text