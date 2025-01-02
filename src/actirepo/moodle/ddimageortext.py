import json

from .question import Question
from actirepo.utils.mime_utils import get_mimetype
from actirepo.utils.image_utils import get_image_size, htmlsize

class DDImageOrText(Question):
    """
    Drag and drop question with images or text
    """

    def __init__(self, element):
        super().__init__(element)
        background_file = element.find('file')
        self.background = f"data:{get_mimetype(background_file)};{background_file.get('encoding')},{background_file.text}"
        self.drags = {
            int(drag.find('no').text) : {
                "no": int(drag.find('no').text),
                "text": drag.find('text').text,
                "type": "text" if drag.find('file') is None else "image",
                "image": f"data:{get_mimetype(drag.find('file'))};{drag.find('file').get('encoding')},{drag.find('file').text}" if drag.find('file') is not None else None,
                "size": self.__drop_text_size(drag.find('text').text) if not drag.find('file') else get_image_size(drag.find('file')),
                "draggroup": int(drag.find('draggroup').text)
            } for drag in element.findall('drag')
        }
        self.drops = {
            int(drop.find('choice').text) : {
                "no": int(drop.find('no').text),
                "text": drop.find('text').text,
                "choice": int(drop.find('choice').text),
                "xleft": int(drop.find('xleft').text),
                "ytop": int(drop.find('ytop').text)
            } for drop in element.findall('drop')
        }
        # add drag sizes to drops
        for choice, drop in self.drops.items():
            drop['size'] = self.drags[choice]['size']
        # group drags by draggroup
        self.draggroups = {}
        for drag in self.drags.values():
            if not drag['draggroup'] in self.draggroups:
                self.draggroups[drag['draggroup']] = [ drag['no'] ]
            else:
                self.draggroups[drag['draggroup']].append(drag['no'])
        # get max width and height for each draggroup
        self.draggroups_size = {}
        for draggroup, drags in self.draggroups.items():
            max_width = 0
            max_height = 0
            for drag_no in drags:
                drag_size = self.drags[drag_no]['size']
                if drag_size['width'] > max_width:
                    max_width = drag_size['width']
                if drag_size['height'] > max_height:
                    max_height = drag_size['height']
            self.draggroups_size[draggroup] = {
                "width": max_width,
                "height": max_height
            }
    
    # get size of text
    def __drop_text_size(self, text):
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

