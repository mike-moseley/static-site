import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Hello, world!")
        self.assertEqual(node.to_html(), "<div>Hello, world!</div>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">Click me!</a>')

    def test_leaf_to_html_img(self):
        node = LeafNode("img", None, {"src": "https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp", "alt": "Boots"})
        self.assertEqual(node.to_html(), '<img src="https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp" alt="Boots">')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_many_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        sibling_nodes = [
            ParentNode("span", [grandchild_node]),
            grandchild_node,
            LeafNode("img", None, {"src": "https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp", "alt": "Boots"})
        ]
        parent_node = ParentNode("div", sibling_nodes)
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><b>grandchild</b></span><b>grandchild</b><img src="https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp" alt="Boots"></div>'
        )
    def test_to_html_with_no_children(self):
        parent_node = ParentNode("b", [LeafNode(None, "SINK")])
        self.assertEqual(
            parent_node.to_html(),
            "<b>SINK</b>"
        )
