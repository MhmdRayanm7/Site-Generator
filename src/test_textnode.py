import unittest
from textnode import TextNode, TextType , text_node_to_html_node , split_nodes_delimiter



class TestTextNode(unittest.TestCase):
    #Text node tests "5"
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


    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    # TextNode to an HTMLNode test "7"

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")


    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")


    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")


    def test_link(self):
        node = TextNode(
            "Google",
            TextType.LINK,
            "https://www.google.com",
        )
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(
            html_node.props,
            {"href": "https://www.google.com"},
        )


    def test_image(self):
        node = TextNode(
            "A cat",
            TextType.IMAGE,
            "https://example.com/cat.png",
        )
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://example.com/cat.png",
                "alt": "A cat",
            },
        )


    def test_invalid_text_type(self):
        node = TextNode("Invalid", "invalid")

        with self.assertRaises(Exception):
            text_node_to_html_node(node)
            
            
    #Split Delimiter "4"

    def test_split_code(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT,
        )

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(result, expected)


    def test_split_multiple_bold(self):
        node = TextNode(
            "This is **bold** and this is **also bold**",
            TextType.TEXT,
        )

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and this is ", TextType.TEXT),
            TextNode("also bold", TextType.BOLD),
        ]

        self.assertEqual(result, expected)


    def test_non_text_node_is_not_split(self):
        node = TextNode("already bold", TextType.BOLD)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result, [node])
        self.assertIs(result[0], node)


    def test_missing_closing_delimiter(self):
        node = TextNode(
            "This has an `unclosed code block",
            TextType.TEXT,
        )

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)
    
    
if __name__ == "__main__":
    unittest.main()     