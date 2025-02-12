import unittest
from marktoblocks import markdown_to_blocks, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):
    def test_empty_string(self):
        markdown = ""
        expected_blocks = []
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_single_block(self):
        markdown = "This is a single block."
        expected_blocks = ["This is a single block."]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_multiple_blocks(self):
        markdown = "This is the first block.\n\nThis is the second block."
        expected_blocks = ["This is the first block.", "This is the second block."]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_blocks_with_whitespace(self):
        markdown = "  This is the first block.  \n\n  This is the second block.  "
        expected_blocks = ["This is the first block.", "This is the second block."]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_blocks_with_empty_lines(self):
        markdown = "This is the first block.\n\n\n\nThis is the second block."
        expected_blocks = ["This is the first block.", "This is the second block."]
        self.assertEqual(markdown_to_blocks(markdown), expected_blocks)

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), "heading")

    def test_code_block(self):
        block = "```\nThis is a code block\n```"
        self.assertEqual(block_to_block_type(block), "code")

    def test_quote(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_ordered_list(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_paragraph(self):
        block = "This is a paragraph."
        self.assertEqual(block_to_block_type(block), "paragraph")

if __name__ == "__main__":
    unittest.main()