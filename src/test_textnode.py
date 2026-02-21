import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a link", TextType.LINK, "www.www.org")
        node2 = TextNode("This is a link", TextType.LINK, "www.www.org")
        self.assertEqual(node, node2)

    def test_text_neq(self):
        node = TextNode("Text", TextType.TEXT)
        node2 = TextNode("Different", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_type_neq(self):
        node = TextNode("Text", TextType.TEXT)
        node2 = TextNode("Text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

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
if __name__ == "__main__":
    unittest.main()
