import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a paragraph" )
        node2 = HTMLNode("p", "This is a paragraph" )
        self.assertEqual(node, node2)

    def test_diff_tag(self):
        node = HTMLNode("a", "This is not a paragraph")
        node2 = HTMLNode("h1","This is not a paragraph")
        self.assertNotEqual(node, node2)

    def test_diff_value(self):
        node = HTMLNode("p", "This is a paragraph")
        node2 = HTMLNode("p", "This is a different paragraph")
        self.assertNotEqual(node, node2)

    def test_diff_children(self):
        child = HTMLNode("p", "This is a child paragraph of a div")
        child2 = HTMLNode("h1", "This is a child heading of another div")
        node = HTMLNode("div", None, child)
        node2 = HTMLNode("div", None, child2)
        self.assertNotEqual(node, node2)

    def test_diff_props(self):
        node = HTMLNode("a", "This is a great website", None, {"href": "https://www.boot.dev"})
        node2 = HTMLNode("a", "This is a great website", None, {"href": "https://archlinux.org"})
        self.assertNotEqual(node, node2)
