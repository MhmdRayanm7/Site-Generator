import unittest

from block_markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):

#Markdown To Blocks '4'

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\n"
                "This is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_removes_extra_empty_blocks(self):
        md = """
# Heading



Paragraph
        """

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph",
            ],
        )

    def test_strips_whitespace(self):
        md = "   First block   \n\n   Second block   "

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block",
            ],
        )

    def test_empty_markdown(self):
        blocks = markdown_to_blocks("")

        self.assertEqual(blocks, [])


if __name__ == "__main__":
    unittest.main()