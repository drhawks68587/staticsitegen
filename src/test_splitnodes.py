import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_single_node(self):
        nodes = [TextNode("This is a text node", TextType.NORMAL_TEXT)]
        delimiter = TextNode(" ", TextType.NORMAL_TEXT)
        result = split_nodes_delimiter(nodes, delimiter)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is a text node")

    def test_split_multiple_nodes(self):
        nodes = [
            TextNode("This is", TextType.NORMAL_TEXT),
            TextNode("a text node", TextType.NORMAL_TEXT)
        ]
        delimiter = TextNode(" ", TextType.NORMAL_TEXT)
        result = split_nodes_delimiter(nodes, delimiter)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is")
        self.assertEqual(result[1].text, " ")
        self.assertEqual(result[2].text, "a text node")

    def test_split_with_no_delimiter(self):
        nodes = [TextNode("This is a text node", TextType.NORMAL_TEXT)]
        delimiter = TextNode(",", TextType.NORMAL_TEXT)
        result = split_nodes_delimiter(nodes, delimiter)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is a text node")

    def test_split_with_multiple_delimiters(self):
        nodes = [
            TextNode("This,is,a,text,node", TextType.NORMAL_TEXT)
        ]
        delimiter = TextNode(",", TextType.NORMAL_TEXT)
        result = split_nodes_delimiter(nodes, delimiter)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "This")
        self.assertEqual(result[1].text, "is")
        self.assertEqual(result[2].text, "a")
        self.assertEqual(result[3].text, "text")
        self.assertEqual(result[4].text, "node")

if __name__ == "__main__":
    unittest.main()