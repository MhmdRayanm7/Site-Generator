import unittest

from block_markdown import (
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
    markdown_to_html_node,
)


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
        
    # Markdown To HTML '5'

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
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and "
            "<code>code</code> here</p></div>",
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
            "<div><pre><code>This is text that _should_ remain\n"
            "the **same** even with inline stuff\n"
            "</code></pre></div>",
        )
    
def test_heading_to_html(self):
    md = """
## This is **bold** heading
"""

    node = markdown_to_html_node(md)
    html = node.to_html()

    self.assertEqual(
        html,
        "<div><h2>This is <b>bold</b> heading</h2></div>",
    )


def test_quote_to_html(self):
    md = """
> This is a quote
> with _italic_ text
"""

    node = markdown_to_html_node(md)
    html = node.to_html()

    self.assertEqual(
        html,
        "<div><blockquote>This is a quote with <i>italic</i> text</blockquote></div>",
    )


def test_lists_to_html(self):
    md = """
- First **item**
- Second item

1. First ordered item
2. Second `ordered` item
"""

    node = markdown_to_html_node(md)
    html = node.to_html()

    self.assertEqual(
        html,
        "<div>"
        "<ul><li>First <b>item</b></li><li>Second item</li></ul>"
        "<ol><li>First ordered item</li><li>Second <code>ordered</code> item</li></ol>"
        "</div>",
    )




if __name__ == "__main__":
    unittest.main()