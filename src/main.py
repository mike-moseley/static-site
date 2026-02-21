import textnode
from textnode import TextNode, TextType, split_nodes_delimiter



def main():
    node = TextNode("blabber", textnode.TextType.CODE)
    print(node)
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    print(new_nodes)
    print(split_nodes_delimiter([], "", TextType.BOLD))


main()
