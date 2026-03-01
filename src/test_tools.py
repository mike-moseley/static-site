import unittest
from textnode import TextNode,TextType
from tools import BlockType
from tools import text_node_to_html_node,split_nodes_delimiter,extract_markdown_images,extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, extract_title

class TestTextNode(unittest.TestCase):
    # Test text_node_to_html_node
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_url(self):
        node = TextNode("This is a text node", TextType.LINK, "archlinux.org")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props["href"], "archlinux.org")

    def test_img(self):
        node = TextNode("Boots", TextType.IMAGE, "https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props["alt"], "Boots")
        self.assertEqual(html_node.props["src"], "https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp")

    #Test split_node_delimiter
    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,[
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ])
    def test_split_list(self):
        nodes = [
            TextNode("This is a text node with no blocks", TextType.TEXT),
            TextNode("**This whole node is bold**", TextType.BOLD),
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("This node has _italic words_", TextType.TEXT)
        ]
        split = split_nodes_delimiter(nodes, '`', TextType.CODE)
        split = split_nodes_delimiter(split, "**", TextType.BOLD)
        split = split_nodes_delimiter(split, "_", TextType.ITALIC)
        self.assertEqual(split,
                         [
                            TextNode("This is a text node with no blocks", TextType.TEXT),
                            TextNode("**This whole node is bold**", TextType.BOLD),
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT),
                            TextNode("This node has ", TextType.TEXT),
                            TextNode("italic words", TextType.ITALIC)
                         ])
    def test_empty(self):
        self.assertEqual(split_nodes_delimiter([], '', TextType.BOLD),[])

    # Test extract_markdown_images
    def test_extract_markdown_images_one(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_images_two(self):
        matches = extract_markdown_images(
            "This is Boots ![image](https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp) just look at that mug!"
        )

    # Test extract_markdown_links
    def test_extract_markdown_links_one(self):
        matches = extract_markdown_links("This is text with a [link](archlinux.org)")
        self.assertListEqual([("link","archlinux.org")],matches)

    def test_extract_markdown_links_two(self):
        matches = extract_markdown_links("This is my [boot.dev profile](https://www.boot.dev/u/mi-mos)")
        self.assertListEqual([("boot.dev profile", "https://www.boot.dev/u/mi-mos")], matches)

    # Test split_nodes_image
    def test_split_nodes_image_end(self):
        matches = split_nodes_image(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
            ]
        )
        self.assertListEqual(matches, 
                             [
                             TextNode("This is text with an ", TextType.TEXT),
                             TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
                             ])
    def test_split_nodes_image_beginning(self):
        matches = split_nodes_image(
            [
                TextNode("![image](https://i.imgur.com/zjjcJKZ.png) at the beginning", TextType.TEXT)
            ]
        )
        self.assertListEqual(matches, 
                             [
                             TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                             TextNode(" at the beginning", TextType.TEXT)
                             ])

    def test_split_nodes_image_no_match_returns_original(self):
        nodes = [TextNode("![image(https://i.imgur.com/zjjcJKZ.png) at the beginning", TextType.TEXT)]
        self.assertListEqual(nodes, split_nodes_image(nodes))

    def test_split_nodes_image_middle(self):
        matches = split_nodes_image(
            [
                TextNode("asdf ![image](https://i.imgur.com/zjjcJKZ.png) at the beginning", TextType.TEXT)
            ]
        )
        self.assertListEqual(matches, 
                             [
                             TextNode("asdf ", TextType.TEXT),
                             TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                             TextNode(" at the beginning", TextType.TEXT)
                             ])
    # I had boots help me for more test coverage...
    def test_split_nodes_image_multiple(self):
        node = TextNode("a ![i1](u1) b ![i2](u2) c", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("a ", TextType.TEXT),
                TextNode("i1", TextType.IMAGE, "u1"),
                TextNode(" b ", TextType.TEXT),
                TextNode("i2", TextType.IMAGE, "u2"),
                TextNode(" c", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_nodes_image_doesnt_touch_non_text(self):
        node = TextNode("![i](u)", TextType.BOLD)  # any non-TEXT
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_nodes_image_mixed_nodes(self):
        nodes = [
            TextNode("no images here", TextType.TEXT),
            TextNode("has ![i](u)", TextType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("no images here", TextType.TEXT),
                TextNode("has ", TextType.TEXT),
                TextNode("i", TextType.IMAGE, "u"),
            ],
            split_nodes_image(nodes),
        )
    def test_split_nodes_link_ignores_images(self):
        node = TextNode("an ![img](u) here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    # Test split_nodes_link
    def test_split_nodes_link_end(self):
        matches = split_nodes_link(
            [
                TextNode("This is text with a [link](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
            ]
        )
        self.assertListEqual(matches, 
                             [
                             TextNode("This is text with a ", TextType.TEXT),
                             TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")
                             ])
    def test_split_nodes_link_beginning(self):
        matches = split_nodes_link(
            [
                TextNode("[link](https://i.imgur.com/zjjcJKZ.png) at the beginning", TextType.TEXT)
            ]
        )
        self.assertListEqual(matches, 
                             [
                             TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                             TextNode(" at the beginning", TextType.TEXT)
                             ])
    def test_split_nodes_link_middle(self):
        matches = split_nodes_link(
            [
                TextNode("asdf [link](https://i.imgur.com/zjjcJKZ.png) at the beginning", TextType.TEXT)
            ]
        )
        self.assertListEqual(matches, 
                             [
                             TextNode("asdf ", TextType.TEXT),
                             TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                             TextNode(" at the beginning", TextType.TEXT)
                             ])
    def test_split_nodes_link_no_match_returns_original(self):
        nodes = [TextNode("[link(https://i.imgur.com/zjjcJKZ.png) at the beginning", TextType.TEXT)]
        self.assertListEqual(nodes, split_nodes_link(nodes))

    # I had boots help me for more test coverage...
    def test_split_nodes_link_multiple(self):
        node = TextNode("a [l1](u1) b [l2](u2) c", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("a ", TextType.TEXT),
                TextNode("l1", TextType.LINK, "u1"),
                TextNode(" b ", TextType.TEXT),
                TextNode("l2", TextType.LINK, "u2"),
                TextNode(" c", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_nodes_link_doesnt_touch_non_text(self):
        node = TextNode("[i](u)", TextType.BOLD)  # any non-TEXT
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_nodes_link_mixed_nodes(self):
        nodes = [
            TextNode("no links here", TextType.TEXT),
            TextNode("has [l](u)", TextType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("no links here", TextType.TEXT),
                TextNode("has ", TextType.TEXT),
                TextNode("l", TextType.LINK, "u"),
            ],
            split_nodes_link(nodes),
        )
    def test_split_nodes_link_ignores_images(self):
        node = TextNode("an ![img](u) here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_text_to_textnodes(self):
        node_list = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        expected_node_list = [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        self.assertListEqual(node_list, expected_node_list)

    def test_text_to_textnodes_empty(self):
        node_list = text_to_textnodes("")
        expected_node_list = []
        self.assertListEqual(node_list, expected_node_list)

    def test_text_to_textnodes_only_text(self):
        node_list = text_to_textnodes("Just a single text node")
        expected_node_list = [
            TextNode("Just a single text node", TextType.TEXT)
        ]
        self.assertListEqual(node_list, expected_node_list)

    def test_text_to_textnodes_only_bold(self):
        node_list = text_to_textnodes("**Just a single text node**")
        expected_node_list = [
            TextNode("Just a single text node", TextType.BOLD)
        ]
        self.assertListEqual(node_list, expected_node_list)

    def test_text_to_textnodes_beginning_italic(self):
        node_list = text_to_textnodes("_Just_ a single text node")
        expected_node_list = [
            TextNode("Just", TextType.ITALIC),
            TextNode(" a single text node", TextType.TEXT)
        ]
        self.assertListEqual(node_list, expected_node_list)

    def test_text_to_textnodes_end_code(self):
        node_list = text_to_textnodes("Just a single text `node`")
        expected_node_list = [
            TextNode("Just a single text ", TextType.TEXT),
            TextNode("node", TextType.CODE)
        ]
        self.assertListEqual(node_list, expected_node_list)

    def test_text_to_textnodes_touching_mixed(self):
        node_list = text_to_textnodes("_touching_`mixed`")
        expected_node_list = [
            TextNode("touching", TextType.ITALIC),
            TextNode("mixed", TextType.CODE),
        ]
        self.assertListEqual(node_list, expected_node_list)

    def test_text_to_textnodes_nested(self):
        node_list = text_to_textnodes("**Just a `single` text node**")
        expected_node_list = [
            TextNode("Just a `single` text node", TextType.BOLD)
        ]
        self.assertListEqual(node_list, expected_node_list)

    # Test markdown_to_blocks
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks_multiple_newlines(self):
        md = "Zoinks\n\n\n  **Scoob**"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Zoinks","**Scoob**"])
    def test_markdown_to_blocks_empty_after_strip(self):
        md = "Where's\n\n \n \n\n my scooby snack?"
        expected = ["Where's", "my scooby snack?"]
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, expected)

    # Test block_to_block_type
    def test_block_to_block_type_plain_valid(self):
        md = "Just a normal paragraph"
        expected = BlockType.PARAGRAPH

        self.assertEqual(block_to_block_type(md), expected)

    def test_block_to_block_type_heading_valid(self):
        md = "### This is a Heading"
        expected = BlockType.HEADING

        self.assertEqual(block_to_block_type(md), expected)

    def test_block_to_block_type_heading_invalid(self):
        md = "- This is an unordered list"
        expected = BlockType.HEADING

        self.assertNotEqual(block_to_block_type(md), expected)

    def test_block_to_block_type_heading_one(self):
        md = "# This is a Heading"
        expected = BlockType.HEADING

        self.assertEqual(block_to_block_type(md), expected)

    def test_block_to_block_type_heading_six(self):
        md = "###### This is a Heading"
        expected = BlockType.HEADING

        self.assertEqual(block_to_block_type(md), expected)

    def test_block_to_block_type_heading_seven(self):
        md = "####### This is not a Heading"
        expected = BlockType.HEADING

        self.assertNotEqual(block_to_block_type(md), expected)

    def test_block_to_block_type_heading_no_space(self):
        md = "###This is a Heading"
        expected = BlockType.HEADING

        self.assertNotEqual(block_to_block_type(md), expected)

    def test_block_to_block_type_code_valid(self):
        md = """```
This is a code block
```"""
        result = block_to_block_type(md)
        expected = BlockType.CODE

        self.assertEqual(result, expected)

    def test_block_to_block_type_code_not_code(self):
        md = "### This is a Heading"
        result = block_to_block_type(md)
        expected = BlockType.CODE

        self.assertNotEqual(result, expected)

    def test_block_to_block_type_code_no_nl(self):
        md = """```This is a code block
```"""
        result = block_to_block_type(md)
        expected = BlockType.CODE

        self.assertNotEqual(result, expected)

    def test_block_to_block_type_code_no_close(self):
        md = """```This is a code block
"""
        result = block_to_block_type(md)
        expected = BlockType.CODE

        self.assertNotEqual(result, expected)

    def test_block_to_block_type_quote(self):
        md = "> This is a \n>valid\n> quote block"
        result = block_to_block_type(md)
        expected = BlockType.QUOTE

        self.assertEqual(result, expected)

    def test_block_to_block_type_quote_not_quote(self):
        md = """```This is a code block
```"""
        result = block_to_block_type(md)
        expected = BlockType.QUOTE

        self.assertNotEqual(result, expected)

    def test_block_to_block_type_quote_invalid(self):
        md = "> This is a quote\nThis is not"
        result = block_to_block_type(md)
        expected = BlockType.QUOTE

        self.assertNotEqual(result, expected)

    def test_block_to_block_type_ul(self):
        md = "- Ding\n- Dong\n- An unordered list"
        result = block_to_block_type(md)
        expected = BlockType.UNORDERED_LIST

        self.assertEqual(result, expected)

    def test_block_to_block_type_ul_invalid(self):
        md = "- Ding\n- Dong\n-- Not an unordered list"
        result = block_to_block_type(md)
        expected = BlockType.UNORDERED_LIST

        self.assertNotEqual(result, expected)

    def test_block_to_block_type_ol(self):
        md = "1. Ding\n2. Dong\n3. An ordered list"
        result = block_to_block_type(md)
        expected = BlockType.ORDERED_LIST

        self.assertEqual(result, expected)

    def test_block_to_block_type_ol_0(self):
        md = "0. Ding\n1. Dong\n2. An ordered list"
        result = block_to_block_type(md)
        expected = BlockType.ORDERED_LIST

        self.assertNotEqual(result, expected)

    def test_block_to_block_type_ol_2(self):
        md = "2. Ding\n3. Dong\n4. An ordered list"
        result = block_to_block_type(md)
        expected = BlockType.ORDERED_LIST

        self.assertNotEqual(result, expected)

    def test_block_to_block_type_ol_skip(self):
        md = "1. Ding\n3. Dong\n4. An ordered list"
        result = block_to_block_type(md)
        expected = BlockType.ORDERED_LIST

        self.assertNotEqual(result, expected)

    def test_block_to_block_type_ol_helper_test(self):
        md = ""
        result = block_to_block_type(md)
        expected = BlockType.ORDERED_LIST

        self.assertNotEqual(result, expected)

    def test_extract_title_heading_raises(self):
        with self.assertRaisesRegex(Exception, r"No h1 header found"):
            extract_title("### This is a Heading")

    def test_extract_title_heading(self):
        md = "# This is a Heading"
        result = extract_title(md)
        expected = "This is a Heading"

        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
