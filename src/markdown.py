from blocks import *
from textnode import *
from htmlnode import *

def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    result = "<div>"
    for block in blocks:
        block_type = block_to_block_type(block)
        block = strip_lines(block, block_type)
        block_inline = text_to_textnodes(block)
        block_nodes = []
        for textnode in block_inline:
            block_nodes.append(text_node_to_html_node(textnode))
        block_nodes = block_to_html_node(block_nodes, block_type)
        html = block_nodes.to_html()
        result = f"{result}{html}"
    result = f"{result}</div>"
    return result

def strip_lines(block, block_type):
    lines = block.split("\n")
    result = ""
    count = 0
    for line in lines:
        if block_type == block_type_code:
            line = line.lstrip("`").rstrip("`")
        if block_type == block_type_quote:
            line = line.lstrip("> ")
        if block_type == block_type_olist:
            count += 1
            line = line.lstrip(f"{count}. ")
            line = f"<li>{line}</li>"
        if block_type == block_type_ulist:
            line = line.lstrip("*").lstrip("-").lstrip()
            line = f"<li>{line}</li>"
        result = f"{result}{line} "
    return result.strip(" ")

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_heading:
            words = block.split()
            if len(words[0]) == 1:
                return " ".join(words[1:])