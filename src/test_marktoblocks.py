import unittest
from marktoblocks import markdown_to_blocks

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

if __name__ == "__main__":
    unittest.main()