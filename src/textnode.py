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
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    results = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:  # Changed this line
            results.append(node)
            continue
            
        text = node.text
        delimiter_index = text.find(delimiter)

        if delimiter_index == -1:
            results.append(node)
            continue
            
        start_search_index = delimiter_index + len(delimiter)
        closing_index = text.find(delimiter, start_search_index)
        if closing_index == -1:
            raise ValueError("no closing delimiter found!")
        
        before = text[:delimiter_index]
        between = text[delimiter_index + len(delimiter):closing_index]
        after = text[closing_index + len(delimiter):]

        if before:
            results.append(TextNode(before, TextType.NORMAL_TEXT))
        if between:
            results.append(TextNode(between, text_type))
        if after:
            results.append(TextNode(after, TextType.NORMAL_TEXT))
    return results

def extract_markdown_images(text):
    # Match markdown images: ![alt text](URL)
    pattern = r"!\[([^\[\]]+)\]\(([^\(\)]+)\)"
    matches = re.findall(pattern, text)

    # Return a list of dictionaries instead of tuples
    return [{'alt': alt_text, 'src': url} for alt_text, url in matches]
def extract_markdown_links(text):
    # Match markdown links: [text](URL)
    pattern = r"\[([^\[\]]+)\]\(([^\(\)]+)\)"
    matches = re.findall(pattern, text)

    # Return a list of dictionaries instead of tuples
    return [{'text': link_text, 'href': url} for link_text, url in matches]

def split_nodes_image(old_nodes):
    image_nodes = []  # List for image nodes
    other_nodes = []  # List for non-image nodes

    for node in old_nodes:
        if node.text_type == TextType.NORMAL_TEXT:
            images = extract_markdown_images(node.text)
            if images:
                remaining_text = node.text

                for image in images:
                    full_markdown = f"![{image['alt']}]({image['src']})"
                    parts = remaining_text.split(full_markdown, 1)
                    before = parts[0]
                    remaining_text = parts[1] if len(parts) > 1 else ""

                    # Add non-image text to "others"
                    if before:
                        other_nodes.append(TextNode(before, TextType.NORMAL_TEXT))
                    
                    # Add image node to "image_nodes"
                    image_nodes.append(TextNode(image['alt'], TextType.IMAGES, image['src']))

                # Add remaining text to "others"
                if remaining_text:
                    other_nodes.append(TextNode(remaining_text, TextType.NORMAL_TEXT))
            else:
                other_nodes.append(node)
        else:
            other_nodes.append(node)

    return image_nodes, other_nodes


def split_nodes_link(old_nodes):
    link_nodes = []
    other_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL_TEXT:
            links = extract_markdown_links(node.text)
            if links:
                remaining_text = node.text
                for link in links:
                    full_markdown = f"[{link['text']}]({link['href']})"

                    # Split the text into `before` and `remaining_text`
                    parts = remaining_text.split(full_markdown, 1)
                    before = parts[0]
                    remaining_text = parts[1] if len(parts) > 1 else ""

                    # Add non-link text (before) to "others"
                    if before.strip():
                        other_nodes.append(TextNode(before, TextType.NORMAL_TEXT))
                    
                    # Add link nodes to "link_nodes"
                    link_nodes.append(TextNode(link['text'], TextType.LINKS, link['href']))

                # Add whatever text remains to "others"
                if remaining_text.strip():
                    other_nodes.append(TextNode(remaining_text, TextType.NORMAL_TEXT))
            else:
                other_nodes.append(node)  # No links found, keep node in "others"
        else:
            other_nodes.append(node)  # Non-normal text gets added to "others"
    return link_nodes, other_nodes

def text_to_textnodes(text):
    # Start with a single text node
    nodes = [TextNode(text, TextType.NORMAL_TEXT)]
    
    # Handle images
    image_nodes, other_nodes = split_nodes_image(nodes)
    nodes = other_nodes + image_nodes
    
    # Handle links
    link_nodes, other_nodes = split_nodes_link(nodes)
    nodes = other_nodes + link_nodes
    
    # Handle other delimiters
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC_TEXT)
    
    return nodes




        




