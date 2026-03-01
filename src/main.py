import textnode
from textnode import TextNode, TextType
from tools import markdown_to_html_node, generate_dir, generate_page, generate_pages_recursive
import shutil
import os
import sys


def main():
    base_path = sys.argv[1]
    if os.path.exists("docs/"):
        shutil.rmtree("docs/")
    os.mkdir("docs/")
    generate_dir("static/", "docs/")
    generate_pages_recursive("content/","template.html","docs/",base_path)


main()
