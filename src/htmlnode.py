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
