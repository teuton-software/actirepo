from .question import Question
from actirepo.utils.mime_utils import get_mimetype

class DDMarker(Question):
    """
    Class to manage Drag and Drop Marker questions
    """

    def __init__(self, element):
        super().__init__(element)        
        self.drags = [
            {
                "no": int(drag.find('no').text),
                "text": drag.find('text').text
            } for drag in element.findall('drag')
        ]
        background_file = element.find('file')
        self.background = f"data:{get_mimetype(background_file.get('name'))};{background_file.get('encoding')},{background_file.text}"
