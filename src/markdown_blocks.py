import re

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
      if not (lines[0].startswith("- ") or lines[0].startswith("* ")):
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
