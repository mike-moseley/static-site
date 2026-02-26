import textnode
from textnode import TextNode, TextType
from tools import markdown_to_html_node


def main():
    f = open("boots.md")
    md = f.read()
    node = markdown_to_html_node(md)
    print(f"{node.to_html()}\n")
    f.close()

main()
