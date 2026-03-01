import textnode
from textnode import TextNode, TextType
from tools import markdown_to_html_node, generate_dir, generate_page, generate_pages_recursive
import shutil
import os


def main():
    if os.path.exists("public/"):
        shutil.rmtree("public/")
    os.mkdir("public/")
    generate_dir("static/", "public/")
    generate_pages_recursive("content/","template.html","public/")


main()
