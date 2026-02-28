from enum import Enum
from htmlnode import HTMLNode,LeafNode, ParentNode
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
        b = b.strip()
        if not b:
            continue
        matched_lines = []
        lines = b.splitlines()
        i = 0
        if (lines[0]).strip().startswith('>'):
            match = r"(?:^>)"
        elif (lines[0].strip().startswith("- ")):
            match = r"(?:^- )"
        elif (re.match(r"^\d+\.",lines[0].strip())):
            match = r"(?:^\d+\.\s)"
        else:
            new_blocks.append(b)
            continue

        while(i<len(lines) and re.match(match,lines[i].lstrip())):
            matched_lines.append(lines[i])
            i += 1
        new_blocks.append('\n'.join(matched_lines).strip())
        remainder = '\n'.join(lines[i:]).strip()
        if remainder:
            new_blocks.extend(markdown_to_blocks(remainder))
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
    is_quote = False
    split = block.splitlines()
    for b in split:
        if not b.strip(): continue
        if b.lstrip().startswith('>'):
            is_quote = True
        else:
            return False
    return is_quote

def _block_to_block_ul_helper(block):
    is_ul = False
    split = block.splitlines()
    for b in split:
        if not b.strip(): continue
        if b.lstrip().startswith(f'- '):
            is_ul = True
        else:
            return False
    return is_ul


def _block_to_block_ol_helper(block):
    is_ol = False
    split = block.splitlines()
    i = 0
    for b in split:
        i += 1
        if b.startswith(f'{i}. '):
            is_ol = True
        else:
            return False
    return is_ol

def _count_heading_level(block):
    count = 0
    while count < len(block) and block[count] == "#":
        count += 1
    return count

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_list = []
    for b in blocks:
        tag = ""
        block_type = block_to_block_type(b)
        match block_type:
            case BlockType.HEADING:
                level = _count_heading_level(b)
                tag = f"h{level}"
                md_tag = '#'*level + ' '
                clean_string = b[level:].lstrip()
                children = _text_to_children(clean_string)
                html_list.append(ParentNode(tag, children))
            case BlockType.PARAGRAPH:
                tag = 'p'
                clean_string = _md_to_html_paragraph_helper(b)
                children = _text_to_children(clean_string)
                html_list.append(ParentNode(tag, children))
            case BlockType.QUOTE:
                tag = "blockquote"
                clean_string = _md_to_html_quote_helper(b)
                children = _text_to_children(clean_string)
                html_list.append(ParentNode(tag, children))
            case BlockType.CODE:
                lines = b.splitlines()
                clean_lines = '\n'.join(lines[1:-1]) + '\n'
                html_list.append(ParentNode("pre", [LeafNode("code", clean_lines)]))
            case BlockType.UNORDERED_LIST:
                tag = "ul"
                children = _md_to_html_ul_helper(b)
                html_list.append(ParentNode(tag, children))
            case BlockType.ORDERED_LIST:
                tag = "ol"
                children = _md_to_html_ol_helper(b)
                html_list.append(ParentNode(tag, children))
    return ParentNode("div",html_list)



def _text_to_children(text):
    nodes = text_to_textnodes(text)
    children_list = []
    for n in nodes:
        children_list.append(text_node_to_html_node(n))
    return children_list

def _md_to_html_quote_helper(text):
    lines = text.splitlines()
    clean_lines = []
    for l in lines:
        l = l.lstrip()
        if l.startswith('>'):
            l = l[1:]
            if l.startswith(' '):
                l = l[1:]
        clean_lines.append(l)
    return "\n".join(clean_lines).strip()

def _md_to_html_paragraph_helper(text):
    lines = text.splitlines()
    for l in lines:
        l = l.strip()
    return ' '.join(lines)

def _md_to_html_ul_helper(text):
    lines = text.splitlines()
    li_nodes = []
    for l in lines:
        if not l.strip(): continue
        if not l.startswith("- "):
            raise ValueError("_md_to_html_ul_helper: Not an unordered list!")
        l = l.lstrip()
        li_nodes.append(ParentNode("li", _text_to_children(l[2:])))
    return li_nodes

def _md_to_html_ol_helper(text):
    lines = text.splitlines()
    li_nodes = []
    for l in lines:
        if not l.strip(): continue
        l = l.lstrip()
        if not re.match(r"(?:^\d+\.\s)",l):
            raise ValueError("_md_to_html_ol_helper: Not an ordered list!")
        l = re.sub(r"(?:^\d+\.\s)",'',l, count=1)
        li_nodes.append(ParentNode("li", _text_to_children(l)))
    return li_nodes
