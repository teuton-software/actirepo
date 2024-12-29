from .question import Question
from actirepo.utils.console import format_bytes

class Essay(Question):

    def __init__(self, element):
        super().__init__(element)
        self.editor = element.find('responseformat').text != 'noinline',
        self.response_lines = int(element.find('responsefieldlines').text),
        self.file_upload =  int(element.find('attachments').text) > 0,
        self.max_size = format_bytes(int(element.find('maxbytes').text)) if int(element.find('maxbytes').text) > 0 else "Por defecto",
        self.max_files = int(element.find('attachments').text),
        self.file_types = element.find('filetypeslist').text.split(',') if not element.find('filetypeslist').text is None else []
