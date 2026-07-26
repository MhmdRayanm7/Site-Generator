import unittest

from block_markdown import markdown_to_blocks , BlockType, block_to_block_type


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

    # Test Block To Block '14'

    def test_heading(self):
        self.assertEqual(
            block_to_block_type("### This is a heading"),
            BlockType.HEADING,
        )

    def test_heading_six_hashes(self):
        self.assertEqual(
            block_to_block_type("###### Heading"),
            BlockType.HEADING,
        )

    def test_invalid_heading_without_space(self):
        self.assertEqual(
            block_to_block_type("###Heading"),
            BlockType.PARAGRAPH,
        )

    def test_invalid_heading_seven_hashes(self):
        self.assertEqual(
            block_to_block_type("####### Heading"),
            BlockType.PARAGRAPH,
        )

    def test_code(self):
        block = "```\nprint('Hello')\n```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_invalid_code_without_newline(self):
        block = "```print('Hello')```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_quote(self):
        block = "> First line\n>Second line\n> Third line"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_invalid_quote(self):
        block = "> First line\nSecond line"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_unordered_list(self):
        block = "- First\n- Second\n- Third"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_invalid_unordered_list(self):
        block = "- First\nSecond\n- Third"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_wrong_start(self):
        block = "2. First\n3. Second"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_wrong_sequence(self):
        block = "1. First\n3. Second\n4. Third"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_paragraph(self):
        block = "This is a normal paragraph.\nIt has another line."

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )



if __name__ == "__main__":
    unittest.main()