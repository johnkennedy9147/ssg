import re

from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from parentnode import ParentNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"
block_type_quote = "quote"

def  markdown_to_blocks(markdown):
  blocks = markdown.split('\n\n')
  filtered_blocks = []
  for block in blocks:
    if block == "":
      continue
    filtered_blocks.append(block.lstrip().rstrip("\n"))
  return filtered_blocks

def block_to_block_type(block):
  heading_regex = r"^#{1,6} "
  if re.match(heading_regex, block):
    return block_type_heading
  
  if block.startswith("```") and block.endswith("```"):
        return block_type_code

  lines = block.split("\n")

  if lines[0].startswith(">"):
    for line in lines:
      if not line.startswith(">"):
        return block_type_paragraph
      return block_type_quote
    
  if lines[0].startswith("- ") or lines[0].startswith("* "):
    for line in lines:
      if not (line.startswith("- ") or line.startswith("* ")):
        return block_type_paragraph
      return block_type_ulist
    
  if lines[0].startswith("1. "):
    i = 1
    for line in lines:
      if not line.startswith(f"{i}. "):
        return block_type_paragraph
      i += 1
    return block_type_olist
  return block_type_paragraph

def text_to_text_children(md):
  children = text_to_textnodes(md)
  children_html = []
  for child in children:
    children_html.append(text_node_to_html_node(child))
  return children_html


def html_from_markdown_paragraph(block):
  children = text_to_text_children(block.replace('\n',' ').strip())
  return ParentNode("p", children)

def html_from_markdown_heading(block):
  heading_level = 0
  for char in block:
    if char == '#':
      heading_level += 1
  # would a text splice here be more efficient?
  children = text_to_text_children(block.lstrip('# '))
  return ParentNode(f"h{heading_level}", children)

def html_from_markdown_code(block):
  children = text_to_text_children(block.strip('`'))
  code_tag = ParentNode("code", children)
  return ParentNode("pre", [code_tag])

def html_from_markdown_ordered_list(block):
  lines = block.splitlines()
  children = []
  for line in lines:
    line_children = text_to_text_children(line.lstrip('0123456789. '))
    children.append(ParentNode("li", line_children))
  return ParentNode("ol", children)

def html_from_markdown_unordered_list(block):
  lines = block.replace('- ','').splitlines()
  children = []
  for line in lines:
    line_children = text_to_text_children(line)
    children.append(ParentNode("li", line_children))
  return ParentNode("ul", children)

def html_from_markdown_quote(block):
  cleaned_text = block.replace('> ','').replace('\n', ' ')
  children = text_to_text_children(cleaned_text)
  return ParentNode("blockquote", children)

def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown.strip("\n"))
  children_html=[]
  for block in blocks:
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
      children_html.append(html_from_markdown_paragraph(block))
    if block_type == block_type_heading:
      children_html.append(html_from_markdown_heading(block))
    if block_type == block_type_code:
      children_html.append(html_from_markdown_code(block))
    if block_type == block_type_olist:
      children_html.append(html_from_markdown_ordered_list(block))
    if block_type ==block_type_ulist:
      children_html.append(html_from_markdown_unordered_list(block))
    if block_type == block_type_quote:
      children_html.append(html_from_markdown_quote(block))
  return ParentNode("div", children_html)
