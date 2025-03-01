import re

from htmlnode import *
from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

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
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
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
                split_nodes.append(TextNode(text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = make_new_link_nodes(old_nodes, extract_markdown_images, TextType.IMAGE)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = make_new_link_nodes(old_nodes, extract_markdown_links, TextType.LINK)
    return new_nodes

def make_new_link_nodes(old_nodes, func, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = func(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            delimiter = f"[{link[0]}]({link[1]})"
            if text_type == TextType.IMAGE:
                delimiter = f"!{delimiter}"
                text_list = node.text.split(delimiter, 1)
            else:
                text_list = node.text.split(delimiter, 1)
            if len(text_list) != 2:
                raise ValueError(f"Invalid markdown, {text_type} section not closed")
            if text_list[0] != "":
                new_nodes.append(TextNode(text_list[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], text_type, link[1]))
            node.text = text_list[1]
        if node.text != "":
            new_nodes.append(TextNode(node.text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)  # Process images first
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    return nodes