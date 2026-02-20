import unittest

from textnode import TextNode, TextType


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
        node = TextNode("Text", TextType.PLAIN)
        node2 = TextNode("Different", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_type_neq(self):
        node = TextNode("Text", TextType.PLAIN)
        node2 = TextNode("Text", TextType.ITALIC)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
