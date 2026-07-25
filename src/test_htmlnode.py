import unittest
from htmlnode import HTMLNode , LeafNode , ParentNode


class TestHTMLNode(unittest.TestCase):
    #HTML node tests "3"

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

    #leaf node tests "4"

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


    #Parent Node tests "6"

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

    def test_to_html_with_multiple_children(self):
        parent_node = ParentNode(
            "div",
            [
                LeafNode("p", "First"),
                LeafNode("p", "Second"),
            ],
        )

        self.assertEqual(
            parent_node.to_html(),
            "<div><p>First</p><p>Second</p></div>",
        )


    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(
            "div",
            [child_node],
            {"class": "container"},
        )

        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )


    def test_to_html_without_tag(self):
        parent_node = ParentNode(None, [LeafNode("p", "Hello")])

        with self.assertRaises(ValueError):
            parent_node.to_html()


    def test_to_html_without_children(self):
        parent_node = ParentNode("div", None)

        with self.assertRaises(ValueError):
            parent_node.to_html()
    

if __name__ == "__main__":
    unittest.main()