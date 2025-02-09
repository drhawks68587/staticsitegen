from textnode import *
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props 
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if not self.props:  # Check for None or an empty dictionary
            return ""
        return " " + " ".join([f'{key}="{value}"' for key, value in self.props.items()])
    def __repr__(self):
        parts = []
        if self.tag is not None:
            parts.append(f'tag="{self.tag}"')
        if self.value is not None:
            parts.append(f'value="{self.value}"')
        if self.children is not None:
            parts.append(f'children={self.children}')
        if self.props is not None:
            parts.append(f'props={self.props}')
        return f"HTMLNode({', '.join(parts)})"
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("The 'value' argument is required for LeafNode.")
        if props is None:
            props = {}
        super().__init__(tag=tag, value=value, children=None, props=props)
        self.children = None #no children
    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("All parent nodes must have a tag.")
        if children is None:
            raise ValueError("All parent nodes must have children.")
        if props is None:
            props = {}
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        return f"<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.NORMAL_TEXT:
        return LeafNode(value=text_node.text)
    elif text_node.text_type == TextType.BOLD_TEXT:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC_TEXT:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE_TEXT:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINKS:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGES:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unknown text type: {text_node.text_type}")
