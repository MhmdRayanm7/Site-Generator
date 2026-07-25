import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_with_props(self):
        node = HTMLNode(
            tag="a",
            value="Google",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_empty(self):
        node_none = HTMLNode(tag="p", value="Hello", props=None)
        node_empty = HTMLNode(tag="p", value="Hello", props={})

        self.assertEqual(node_none.props_to_html(), "")
        self.assertEqual(node_empty.props_to_html(), "")


    def test_to_html_raises_error(self):
        node = HTMLNode(tag="p", value="Test")
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()