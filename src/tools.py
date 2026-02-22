from enum import Enum
from htmlnode import HTMLNode,LeafNode
from textnode import TextType, TextNode
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for n in old_nodes:
        if n.text_type is not TextType.TEXT:
            new_nodes.append(n)
        else:
            split = n.text.split(delimiter)
            if len(split) % 2 == 0:
                raise Exception("Invalid Markdown syntax")
            for i in range(0, len(split)):
                if split[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(split[i],TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split[i],text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for n in old_nodes:
        remaining_text = n.text
        if n.text_type == TextType.TEXT:
            image = extract_markdown_images(remaining_text)
            if image == []:
                new_nodes.append(n)
                continue
            for i in image:
                sections = remaining_text.split(f"![{i[0]}]({i[1]})",1)
                if len(sections) !=2:
                    raise ValueError("invalid markdown, image section not closed")
                else:
                    before,after = sections
                if before != "":
                    new_nodes.append((TextNode(before,TextType.TEXT)))
                new_nodes.append((TextNode(i[0], TextType.IMAGE, i[1])))
                remaining_text = after
            if remaining_text == "": 
                continue
            new_nodes.append((TextNode(remaining_text,TextType.TEXT)))
        else:
            new_nodes.append(n)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for n in old_nodes:
        remaining_text = n.text
        if n.text_type == TextType.TEXT:
            link = extract_markdown_links(remaining_text)
            if link == []:
                new_nodes.append(n)
                continue
            for l in link:
                sections = remaining_text.split(f"[{l[0]}]({l[1]})",1)
                if len(sections) !=2:
                    raise ValueError("invalid markdown, link section not closed")
                else:
                    before,after = sections
                if before != "":
                    new_nodes.append((TextNode(before,TextType.TEXT)))
                new_nodes.append((TextNode(l[0], TextType.LINK, l[1])))
                remaining_text = after
            if remaining_text == "": 
                continue
            new_nodes.append((TextNode(remaining_text,TextType.TEXT)))
        else:
            new_nodes.append(n)
    return new_nodes

def text_to_textnodes(text):
    nodes = [
        TextNode(text, TextType.TEXT)
    ]
    nodes = split_nodes_delimiter(nodes,'**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,'_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes,'`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    new_blocks = []
    blocks = markdown.split('\n\n')
    for b in blocks:
        stripped = b.strip('\n').strip()
        if stripped == '' or stripped == "":
            continue
        new_blocks.append(stripped)
    return new_blocks

def block_to_block_type(block):
    if re.match(r"^#{1,6}\ ", block):
        return BlockType.HEADING
    elif re.match(r"^(?:`{3}\n).*\n?(?:`{3})$", block, re.DOTALL):
        return BlockType.CODE
    elif _block_to_block_quote_helper(block):
        return BlockType.QUOTE
    elif _block_to_block_ul_helper(block):
        return BlockType.UNORDERED_LIST
    elif _block_to_block_ol_helper(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def _block_to_block_quote_helper(block):
    split = block.split('\n')
    for b in split:
        if b.startswith('>'):
            continue
        else:
            return False
    return True

def _block_to_block_ul_helper(block):
    split = block.split('\n')
    for b in split:
        if b.startswith(f'- '):
            continue
        else:
            return False
    return True


def _block_to_block_ol_helper(block):
    split = block.split('\n')
    i = 0
    for b in split:
        i += 1
        if b.startswith(f'{i}. '):
            continue
        else:
            return False
    return True


