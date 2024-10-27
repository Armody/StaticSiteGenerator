from textnode import *
from markdown import *
import os
import shutil

source = "./static"
destination = "./public"
markdown = "./content"
template = "./template.html"
html_path = "./public"

def main():
    if os.path.exists(destination):
        shutil.rmtree(destination)        
    copy_files(source, destination)
    generate_pages_recursive(markdown, template, html_path)

def copy_files(src, pth):
    if not os.path.exists(pth):
        os.mkdir(pth)
    for src_file in os.listdir(src):
        file_path = os.path.join(src, src_file)
        dest_path = os.path.join(pth, src_file)
        if os.path.isfile(file_path):
            shutil.copy(file_path, dest_path)
        else:
            copy_files(file_path, dest_path)
            
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, encoding="utf-8") as f:
        md = f.read()
    with open(template_path, encoding="utf-8") as t:
        tmp = t.read()
    html = markdown_to_html(md)
    title = extract_title(md)
    result = tmp.replace("{{ Title }}", title).replace("{{ Content }}", html)
    dest_dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    with open(dest_path, "x", encoding="utf-8") as d:
        d.write(result)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for content in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, content)
        dest_path = os.path.join(dest_dir_path, content.replace(".md", ".html"))
        if os.path.isfile(file_path):
            generate_page(file_path, template_path, dest_path)
        else:
            generate_pages_recursive(file_path, template_path, dest_path)


main()