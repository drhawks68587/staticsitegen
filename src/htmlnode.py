class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props 
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if self.props == None:
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