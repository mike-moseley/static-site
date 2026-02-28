import unittest
import htmlnode
from tools import markdown_to_html_node

class TestTextNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>    This is text that _should_ remain\n    the **same** even with inline stuff\n</code></pre></div>",
        )

    # Quote block
    def test_quoteblock_single(self):
        md = "> hello"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>hello</blockquote></div>"
        )
    def test_quoteblock_multi(self):
        md = """ > front space
>no space
> inline > marker
>\n>oops"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>front space\nno space\ninline > marker\n\noops</blockquote></div>"
        )
    # Heading
    def test_heading_multiple(self):
        md = """
# Heading with # in it

## Heading two

### Heading three

#### Heading four

##### Heading five

###### Heading six
        """
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><h1>Heading with # in it</h1><h2>Heading two</h2><h3>Heading three</h3><h4>Heading four</h4><h5>Heading five</h5><h6>Heading six</h6></div>")
    # Unordered list
    def test_unordered_list(self):
        md = """- This is an
- Unordered list
 -This line shouldn't count
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><ul><li>This is an</li><li>Unordered list</li></ul><p>-This line shouldn't count</p></div>")
    # Ordered list
    def test_ordered_list(self):
        md = "1. one\n2. two\n3. three"
        html = markdown_to_html_node(md).to_html()
        expected = "<div><ol><li>one</li><li>two</li><li>three</li></ol></div>"
        self.assertEqual(html, expected)

if __name__ == "__main__":
    unittest.main()
