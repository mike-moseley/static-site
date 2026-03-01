import textnode
from textnode import TextNode, TextType
from tools import markdown_to_html_node, generate_dir, generate_page, generate_pages_recursive
import shutil
import os
import sys


def main():
    if (len(sys.argv) > 1):
        base_path = sys.argv[1]
    else:
        base_path = '/'

    if not base_path.startswith('/'):
        base_path = '/'+base_path
    if not base_path.endswith('/'):
        base_path = '/'+base_path

    if os.path.exists("docs/"):
        shutil.rmtree("docs/")
    os.mkdir("docs/")
    generate_dir("static/", "docs/")
    generate_pages_recursive("content/","template.html","docs/",base_path)


main()
