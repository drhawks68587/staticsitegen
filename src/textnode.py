from enum import Enum
import re

class TextType(Enum):
    NORMAL_TEXT = "text"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINKS = "links"
    IMAGES = "images"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        return (self.text == other.text and 
                self.text_type == other.text_type and 
                self.url == other.url)
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return [url for alt_text, url in matches]  
def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return [url for _, url in matches]

def split_nodes_image(old_nodes):
    split_images = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL_TEXT:
            images = extract_markdown_images(node.text)
            if images:
                remaining_text = node.text
                for url in images:
                    full_markdown = f"![alt text]({url})"

                    parts = remaining_text.split(full_markdown, 1)
                    before = parts[0]
                    remaining_text = parts[1] if len(parts) > 1 else ""

                    if before:
                        split_images.append(TextNode(before, TextType.NORMAL_TEXT))

                    split_images.append(TextNode("", TextType.IMAGES, url))
                if remaining_text:
                    split_images.append(TextNode(remaining_text, TextType.NORMAL_TEXT))
            else:
                split_images.append(node)
        else:
            split_images.append(node)
    return split_images



def split_nodes_link(old_nodes):
    split_links = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL_TEXT:
            links = extract_markdown_links(node.text)
            if links:
                remaining_text = node.text
                for link_text, url in links:
                    full_markdown = f"[{link_text}]({url})"

                    parts = remaining_text.split(full_markdown, 1)
                    before = parts[0]
                    remaining_text = parts[1] if len(parts) > 1 else ""

                    if before:
                        split_links.append(TextNode(before, TextType.NORMAL_TEXT))
                        split_links.append(TextNode(link_text, TextType.LINK, url))

                if remaining_text:
                    split_links.append(TextNode(remaining_text, TextType.NORMAL_TEXT))
            else:
                split_links.append(node)
        else:
            split_links.append(node)
    return split_links

        




