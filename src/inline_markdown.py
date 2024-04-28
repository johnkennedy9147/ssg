from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        # function will have to be called on delimiters in correct order or chaos will ensue
        # eg ** will be matched for *
        # possible solution use re.split here
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
          # handles case where delimiter is first or last piece of text
            if sections[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(sections[i], text_type_text))
            else:
                new_nodes.append(TextNode(sections[i], text_type))
    return new_nodes
