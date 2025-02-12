from htmlnode import *
from textnode import *
import re

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        if block.strip():
            stripped_blocks.append(block.strip())
    return stripped_blocks

def block_to_block_type(block):
    lines = block.split('\n')

    if re.match(r'#{1,6} \S', block):
        return "heading"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    if all(line.startswith(">") for line in lines):
        return "quote"
    if all(re.match(r'^[*-] ', line) for line in lines):
        return "unordered_list"
    if all(re.match(r'\d+\. \S', line) for line in lines):
        numbers = [int(re.match(r'(\d+)\. ', line).group(1)) for line in lines]
        if numbers == list(range(1, len(numbers) + 1)):
            return "ordered_list"
    return "paragraph"
