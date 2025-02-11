from htmlnode import *
from textnode import *

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