import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is another text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_text_content(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node.text, "This is a text node")

    def test_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node.text_type, TextType.BOLD_TEXT)

    def test_change_text(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node.text = "Changed text"
        self.assertEqual(node.text, "Changed text")

    def test_change_type(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node.type = TextType.ITALIC_TEXT
        self.assertEqual(node.type, TextType.ITALIC_TEXT)


if __name__ == "__main__":
    unittest.main()