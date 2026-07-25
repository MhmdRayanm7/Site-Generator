import unittest
from htmlnode import HTMLNode , LeafNode


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

    #leaf node tests

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_tag(self):
        node = LeafNode("p", "Hello")
        self.assertEqual(node.to_html(), "<p>Hello</p>")


    def test_leaf_to_html_without_tag(self):
        node = LeafNode(None, "Hello")
        self.assertEqual(node.to_html(), "Hello")


    def test_leaf_nodes_not_equal(self):
        node1 = LeafNode("p", "Hello")
        node2 = LeafNode("p", "Goodbye")
        self.assertNotEqual(node1.to_html(), node2.to_html())


if __name__ == "__main__":
    unittest.main()