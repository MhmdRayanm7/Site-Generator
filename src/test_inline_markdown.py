import unittest
from textnode import TextNode, TextType

from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnodes ,
)

# Extract Links '5'
class TestInlineMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        text = "Image: ![cat](https://example.com/cat.png)"

        result = extract_markdown_images(text)

        self.assertListEqual(
            [("cat", "https://example.com/cat.png")],
            result,
        )


    def test_extract_multiple_images(self):
        text = "![cat](cat.png) and ![dog](dog.png)"

        result = extract_markdown_images(text)

        self.assertListEqual(
            [("cat", "cat.png"), ("dog", "dog.png")],
            result,
        )


    def test_extract_markdown_links(self):
        text = "Visit [Boot.dev](https://www.boot.dev)"

        result = extract_markdown_links(text)

        self.assertListEqual(
            [("Boot.dev", "https://www.boot.dev")],
            result,
        )


    def test_links_do_not_include_images(self):
        text = "![cat](cat.png) and [website](https://example.com)"

        result = extract_markdown_links(text)

        self.assertListEqual(
            [("website", "https://example.com")],
            result,
        )


    def test_no_matches(self):
        text = "This is normal text"

        self.assertListEqual([], extract_markdown_images(text))
        self.assertListEqual([], extract_markdown_links(text))

# split Links '9'


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )


    def test_split_image_at_start(self):
        node = TextNode(
            "![cat](cat.png) is a cat",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("cat", TextType.IMAGE, "cat.png"),
                TextNode(" is a cat", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_split_image_at_end(self):
        node = TextNode(
            "This is a cat ![cat](cat.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is a cat ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "cat.png"),
            ],
            new_nodes,
        )


    def test_split_no_images(self):
        node = TextNode("Normal text", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertListEqual([node], new_nodes)


    def test_split_image_ignores_non_text_node(self):
        node = TextNode("Already bold", TextType.BOLD)

        new_nodes = split_nodes_image([node])

        self.assertListEqual([node], new_nodes)


    def test_split_links(self):
        node = TextNode(
            "Visit [Boot.dev](https://www.boot.dev) and "
            "[YouTube](https://www.youtube.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "YouTube",
                    TextType.LINK,
                    "https://www.youtube.com",
                ),
            ],
            new_nodes,
        )


    def test_split_link_at_start(self):
        node = TextNode(
            "[Boot.dev](https://www.boot.dev) is useful",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
                TextNode(" is useful", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_split_no_links(self):
        node = TextNode("Normal text", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual([node], new_nodes)


    def test_split_link_does_not_split_image(self):
        node = TextNode(
            "This is ![cat](cat.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual([node], new_nodes)
    
    # Text to Textnodes "5"
        
    def test_text_to_textnodes_full(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        result = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image",
                TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(expected, result)


    def test_text_to_textnodes_plain_text(self):
        result = text_to_textnodes("This is normal text")

        expected = [
            TextNode("This is normal text", TextType.TEXT),
        ]

        self.assertListEqual(expected, result)


    def test_text_to_textnodes_multiple_bold(self):
        result = text_to_textnodes(
            "This is **bold** and **also bold**"
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("also bold", TextType.BOLD),
        ]

        self.assertListEqual(expected, result)


    def test_text_to_textnodes_image_and_link(self):
        result = text_to_textnodes(
            "![cat](cat.png) and [website](https://example.com)"
        )

        expected = [
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "website",
                TextType.LINK,
                "https://example.com",
            ),
        ]

        self.assertListEqual(expected, result)


    def test_text_to_textnodes_unclosed_delimiter(self):
        with self.assertRaises(Exception):
            text_to_textnodes("This is **not closed")