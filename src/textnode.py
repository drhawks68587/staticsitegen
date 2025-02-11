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
    new_nodes = []  # Final list of nodes, preserving order

    for node in old_nodes:
        if node.text_type == TextType.NORMAL_TEXT:
            images = extract_markdown_images(node.text)  # Extract images
            if images:
                remaining_text = node.text  # Start with the full text

                for image in images:
                    # Image markdown to split around
                    full_markdown = f"![{image['alt']}]({image['src']})"

                    # Split text at the image markdown, keeping before and after parts
                    parts = remaining_text.split(full_markdown, 1)
                    before = parts[0]
                    remaining_text = parts[1] if len(parts) > 1 else ""

                    # Add the text before the image markdown (if non-empty)
                    if before:
                        new_nodes.append(TextNode(before, TextType.NORMAL_TEXT))

                    # Create and add the image node
                    new_nodes.append(TextNode(image['alt'], TextType.IMAGES, image['src']))

                # Process any remaining text after the last image
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.NORMAL_TEXT))
            else:
                # No images in text, so add the whole node as-is
                new_nodes.append(node)
        else:
            # Not normal text, so add the whole node as-is
            new_nodes.append(node)

    return new_nodes


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
    nodes = [TextNode(text, TextType.NORMAL_TEXT)]
    new_nodes = []

    for node in nodes: #splitting links
        if node.text_type == TextType.NORMAL_TEXT:
            result = split_nodes_link(node.text)
            new_nodes.extend(result)
        else:
            new_nodes.append(node)
    nodes = new_nodes
    new_nodes = []
    for node in nodes: #splitting images
        if node.text_type == TextType.NORMAL_TEXT:
            result = split_nodes_image(node.text)
            new_nodes.extend(result)
        else:
            new_nodes.append(node)
    nodes = new_nodes
    new_nodes = []
    for node in nodes: #splitting code
        if node.text_type == TextType.NORMAL_TEXT:
            result = split_nodes_delimiter(node.text, "`", TextType.CODE_TEXT)
            new_nodes.extend(result)
        else:
            new_nodes.append(node)
    nodes = new_nodes
    new_nodes = []
    for node in nodes: #splitting bold
        if node.text_type == TextType.NORMAL_TEXT:
            result = split_nodes_delimiter(node.text, "**", TextType.BOLD_TEXT)
            new_nodes.extend(result)
        else:
            new_nodes.append(node)
    nodes = new_nodes
    new_nodes = []
    for node in nodes: #splitting italic
        if node.text_type == TextType.NORMAL_TEXT:
            result = split_nodes_delimiter(node.text, "*", TextType.ITALIC_TEXT)
            new_nodes.extend(result)
        else:
            new_nodes.append(node)
    nodes = new_nodes
    return nodes




        




