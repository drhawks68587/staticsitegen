import unittest
from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(
            nodes,
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" word", TextType.NORMAL_TEXT),
            ]
        )

    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.NORMAL_TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.NORMAL_TEXT),
                TextNode("bold", TextType.BOLD_TEXT),
                TextNode(" text", TextType.NORMAL_TEXT),
            ]
        )

    def test_split_italic(self):
        node = TextNode("This is *italic* text", TextType.NORMAL_TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC_TEXT)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.NORMAL_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" text", TextType.NORMAL_TEXT),
            ]
        )

    def test_multiple_delimiters(self):
        node = TextNode("This is `code` and **bold** text", TextType.NORMAL_TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.NORMAL_TEXT),
                TextNode("code", TextType.CODE_TEXT),
                TextNode(" and **bold** text", TextType.NORMAL_TEXT),
            ]
        )

if __name__ == "__main__":
    unittest.main()