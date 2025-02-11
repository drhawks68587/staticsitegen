import unittest

from textnode import TextNode, TextType
from textnode import extract_markdown_images, extract_markdown_links
from textnode import split_nodes_images, split_nodes_links

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

    def test_extract_markdown_images(self):
        markdown_text = "![alt text](image1.png) ![another image](image2.jpg)"
        expected_images = ["image1.png", "image2.jpg"]
        self.assertEqual(extract_markdown_images(markdown_text), expected_images)

    def test_extract_markdown_links(self):
        markdown_text = "[example](http://example.com) [another link](http://another.com)"
        expected_links = ["http://example.com", "http://another.com"]
        self.assertEqual(extract_markdown_links(markdown_text), expected_links)

    def test_split_nodes_images(self):
        text_nodes = [
            TextNode(text="Image 1", text_type=TextType.IMAGES, url="http://example.com/image1.png"),
            TextNode(text="Normal text", text_type=TextType.NORMAL_TEXT),
            TextNode(text="Image 2", text_type=TextType.IMAGES, url="http://example.com/image2.png")
        ]
        images, others = split_nodes_images(text_nodes)
        
        self.assertEqual(len(images), 2)
        self.assertEqual(len(others), 1)
        self.assertEqual(images[0].url, "http://example.com/image1.png")
        self.assertEqual(images[1].url, "http://example.com/image2.png")
        self.assertEqual(others[0].text, "Normal text")

    def test_split_nodes_links(self):
        text_nodes = [
            TextNode(text="Link 1", text_type=TextType.LINKS, url="http://example.com/link1"),
            TextNode(text="Normal text", text_type=TextType.NORMAL_TEXT),
            TextNode(text="Link 2", text_type=TextType.LINKS, url="http://example.com/link2")
        ]
        links, others = split_nodes_links(text_nodes)
        
        self.assertEqual(len(links), 2)
        self.assertEqual(len(others), 1)
        self.assertEqual(links[0].url, "http://example.com/link1")
        self.assertEqual(links[1].url, "http://example.com/link2")
        self.assertEqual(others[0].text, "Normal text")

if __name__ == "__main__":
    unittest.main()