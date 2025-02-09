import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

class TestLeafNode(unittest.TestCase):
    def test_leaf_node_creation(self):
        node = LeafNode(tag="p", value="This is a paragraph.")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph.")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {})

    def test_leaf_node_to_html(self):
        node = LeafNode(tag="p", value="This is a paragraph.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")

    def test_leaf_node_to_html_with_props(self):
        node = LeafNode(tag="a", value="Click here", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click here</a>')

    def test_leaf_node_without_value(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="p")

class TestParentNode(unittest.TestCase):
    def test_parent_node_creation(self):
        child1 = LeafNode(tag="p", value="Paragraph 1")
        child2 = LeafNode(tag="p", value="Paragraph 2")
        node = ParentNode(tag="div", children=[child1, child2])
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, [child1, child2])
        self.assertEqual(node.props, {})

    def test_parent_node_to_html(self):
        child1 = LeafNode(tag="p", value="Paragraph 1")
        child2 = LeafNode(tag="p", value="Paragraph 2")
        node = ParentNode(tag="div", children=[child1, child2])
        self.assertEqual(node.to_html(), "<div><p>Paragraph 1</p><p>Paragraph 2</p></div>")

    def test_parent_node_to_html_with_props(self):
        child1 = LeafNode(tag="p", value="Paragraph 1")
        child2 = LeafNode(tag="p", value="Paragraph 2")
        node = ParentNode(tag="div", children=[child1, child2], props={"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><p>Paragraph 1</p><p>Paragraph 2</p></div>')

    def test_parent_node_without_tag(self):
        child1 = LeafNode(tag="p", value="Paragraph 1")
        child2 = LeafNode(tag="p", value="Paragraph 2")
        with self.assertRaises(ValueError):
            ParentNode(tag=None, children=[child1, child2])

    def test_parent_node_without_children(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="div", children=None)

if __name__ == "__main__":
    unittest.main()