import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links

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