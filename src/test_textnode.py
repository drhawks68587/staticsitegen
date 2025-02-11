import unittest

from textnode import TextNode, TextType
from textnode import extract_markdown_images, extract_markdown_links
from textnode import split_nodes_image, split_nodes_link, text_to_textnodes

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
        expected_images = [
            {"alt": "alt text", "src": "image1.png"},
            {"alt": "another image", "src": "image2.jpg"}
        ]
        self.assertEqual(extract_markdown_images(markdown_text), expected_images)

    def test_extract_markdown_links(self):
        markdown_text = "[example](http://example.com) [another link](http://another.com)"
        expected_links = [
            {"text": "example", "href": "http://example.com"},
            {"text": "another link", "href": "http://another.com"}
        ]
        self.assertEqual(extract_markdown_links(markdown_text), expected_links)

    def test_split_nodes_image(self):
        text_nodes = [
            TextNode(text="Normal text with ![Image 1](http://example.com/image1.png) and ![Image 2](http://example.com/image2.png)", text_type=TextType.NORMAL_TEXT),
            TextNode(text="Normal text", text_type=TextType.NORMAL_TEXT)
        ]
        image_nodes, other_nodes = split_nodes_image(text_nodes)
        
        self.assertEqual(len(image_nodes), 2)
        self.assertEqual(image_nodes[0].url, "http://example.com/image1.png")
        self.assertEqual(image_nodes[1].url, "http://example.com/image2.png")
        self.assertEqual(other_nodes[0].text, "Normal text with ")
        self.assertEqual(other_nodes[1].text, " and ")

    def test_split_nodes_link(self):
        text_nodes = [
            TextNode(text="Normal text with [Link 1](http://example.com/link1) and [Link 2](http://example.com/link2)", text_type=TextType.NORMAL_TEXT),
            TextNode(text="Normal text", text_type=TextType.NORMAL_TEXT)
        ]
        links, others = split_nodes_link(text_nodes)
        
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0].url, "http://example.com/link1")
        self.assertEqual(links[1].url, "http://example.com/link2")
        self.assertEqual(others[0].text, "Normal text with ")
        self.assertEqual(others[1].text, " and ")

def test_text_to_textnodes(self):
    text = "Normal text with [Link 1](http://example.com/link1) and [Link 2](http://example.com/link2)"
    expected_nodes = [
        TextNode(text="Normal text with ", text_type=TextType.NORMAL_TEXT),  # Using your NORMAL_TEXT
        TextNode(text="Link 1", text_type=TextType.LINKS, url="http://example.com/link1"),  # Using your LINKS
        TextNode(text=" and ", text_type=TextType.NORMAL_TEXT),  # Using your NORMAL_TEXT
        TextNode(text="Link 2", text_type=TextType.LINKS, url="http://example.com/link2")  # Using your LINKS
    ]
    result_nodes = text_to_textnodes(text)
    
    self.assertEqual(len(result_nodes), len(expected_nodes))
    for result_node, expected_node in zip(result_nodes, expected_nodes):
        self.assertEqual(result_node, expected_node)

if __name__ == "__main__":
    unittest.main()