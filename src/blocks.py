from htmlnode import *
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def markdown_to_blocks(markdown):
    blocks = list(map(lambda block: block.strip(), markdown.split("\n\n")))
    for block in blocks:
        if block == "":
            blocks.remove(block)
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if line_count(lines, ">") == len(lines):
        return BlockType.QUOTE
    if line_count(lines, "* ", "- ") == len(lines):
        return BlockType.ULIST
    if line_count(lines) == len(lines) and not block.startswith("!["):
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def line_count(lines, mark0=None, mark1=None):
    count = 0
    for line in lines:
        if mark0 != None and mark1 != None:
            if line.startswith(mark0) or line.startswith(mark1):
                count += 1
                continue
        if mark0 != None:
            if line.startswith(mark0):
                count += 1
                continue
        if line.startswith(f"{count+1}. ") and mark0 == None:
            count += 1
    return count

def block_to_html_node(children, block_type):
    if block_type == BlockType.PARAGRAPH:
        return ParentNode("p", children)
    if block_type == BlockType.HEADING:
        text_list = children[0].value.split(" ")
        count = len(text_list[0])
        children[0].value = " ".join(text_list[1:])
        return ParentNode(f"h{count}", children)
    if block_type == BlockType.CODE:
        code_block = ParentNode("code", children)
        return ParentNode("pre", [code_block])
    if block_type == BlockType.QUOTE:
        return ParentNode("blockquote", children)
    if block_type == BlockType.OLIST:
        return ParentNode("ol", children)
    if block_type == BlockType.ULIST:
        return ParentNode("ul", children)
    return children