from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)
import re

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

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        text_to_split=node.text
        # exit early if text cannot have a image, min 5 chars required for markdown image ![]()
        if len(text_to_split) < 6:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(text_to_split)
        # handle no images found in text
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            sections = text_to_split.split(f"![{image[0]}]({image[1]})",1)
            # handles case where image is at start of text, or is all of text
            if sections[0]!="":
                new_nodes.append(TextNode(sections[0], text_type_text))
            # append image we split on
            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            #replace text to split with whatever remains if anything
            text_to_split = sections[1]
        # create text node for any remaining text after last image processed
        if len(text_to_split) >0:
            new_nodes.append(TextNode(text_to_split, text_type_text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        text_to_split=node.text
        # exit early if text cannot have a link, min 4 chars required for markdown link []()
        if len(text_to_split) < 5:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(text_to_split)
        # handle no links found in text
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            sections = text_to_split.split(f"[{link[0]}]({link[1]})",1)
            # handles case where link is at start of text, or is all of text
            if sections[0]!="":
                new_nodes.append(TextNode(sections[0], text_type_text))
            # append link we split on
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            #replace text to split with whatever remains if anything
            text_to_split = sections[1]
        # create text node for any remaining text after last link processed
        if len(text_to_split) >0:
            new_nodes.append(TextNode(text_to_split, text_type_text))
    return new_nodes
