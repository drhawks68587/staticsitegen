import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_content(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text, "This is a text node")

    def test_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.type, TextType.BOLD)

    def test_change_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node.text = "Changed text"
        self.assertEqual(node.text, "Changed text")

    def test_change_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node.type = TextType.ITALIC
        self.assertEqual(node.type, TextType.ITALIC)


if __name__ == "__main__":
    unittest.main()