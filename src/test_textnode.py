import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    
    def test_eq(self):

        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node, node2 , "Nodes with the same text and type should be equal")
        
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)

        self.assertNotEqual(node, node2, "Nodes with different text should not be equal")

    def test_link_node(self):
        node = TextNode("Click here", TextType.LINK, url="https://example.com")
        node2 = TextNode("Click here", TextType.LINK, url="https://example.com")

        self.assertEqual(node, node2, "Link nodes with the same text and URL should be equal")

    def test_type_mismatch(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = "Not a TextNode"

        self.assertNotEqual(node, node2, "A TextNode should not be equal to a non-TextNode object")

    def test_typeTextDifferent(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)

        self.assertNotEqual(node, node2, "Nodes with the same text but different types should not be equal")

if __name__ == "__main__":
    unittest.main()