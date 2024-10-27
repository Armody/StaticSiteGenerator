import re

from htmlnode import *

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__ (self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        split_nodes = []
        text_list = node.text.split(delimiter)
        if len(text_list) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i, text in enumerate(text_list):
            if text == "":
                continue
            if i % 2 == 1:
                split_nodes.append(TextNode(text, text_type))
            else:
                split_nodes.append(TextNode(text, text_type_text))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = make_new_link_nodes(old_nodes, extract_markdown_images, text_type_image)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = make_new_link_nodes(old_nodes, extract_markdown_links, text_type_link)
    return new_nodes

def make_new_link_nodes(old_nodes, func, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        links = func(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            delimiter = f"[{link[0]}]({link[1]})"
            if text_type == text_type_image:
                text_list = node.text.split(f"!{delimiter}", 1)
            else:
                text_list = node.text.split(f"{delimiter}", 1)
            if len(text_list) != 2:
                raise ValueError(f"Invalid markdown, {text_type} section not closed")
            if text_list[0] != "":
                new_nodes.extend([TextNode(text_list[0], text_type_text)
                                ,TextNode(link[0], text_type, link[1])])
            node.text = text_list[1]
        if node.text != "":
            new_nodes.append(TextNode(node.text, text_type_text))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes