text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
  def __init__(self, text, text_type, url=None):
    self.text = text
    self.text_type = text_type
    self.url = url

  def __eq__(self, node2):
    return (
            self.text_type == node2.text_type
            and self.text == node2.text
            and self.url == node2.url
        )
  
  def __repr__(self):
    return f'TextNode({self.text}, { self.text_type}, {self.url})'
