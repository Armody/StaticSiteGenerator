from htmlnode import *

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_blocks(markdown):
    blocks = list(map(lambda block: block.strip(), markdown.split("\n\n")))
    for block in blocks:
        if block == "":
            blocks.remove(block)
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    if block.startswith("```") and block.endswith("```"):
        return block_type_code
    if line_count(lines, ">") == len(lines):
        return block_type_quote
    if line_count(lines, "* ", "- ") == len(lines):
        return block_type_ulist
    if line_count(lines) == len(lines):
        return block_type_olist
    return block_type_paragraph

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
    if block_type == block_type_paragraph:
        return ParentNode("p", children)
    if block_type == block_type_heading:
        text_list = children[0].value.split(" ")
        count = len(text_list[0])
        children[0].value = " ".join(text_list[1:])
        return ParentNode(f"h{count}", children)
    if block_type == block_type_code:
        code_block = ParentNode("code", children)
        return ParentNode("pre", [code_block])
    if block_type == block_type_quote:
        return ParentNode("blockquote", children)
    if block_type == block_type_olist:
        return ParentNode("ol", children)
    if block_type == block_type_ulist:
        return ParentNode("ul", children)
    return children