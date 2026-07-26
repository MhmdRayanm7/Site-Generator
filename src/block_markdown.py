from textnode import TextNode, TextType
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    new_blocks = []

    for block in blocks:
        block = block.strip()

        if block != "":
            new_blocks.append(block)

    return new_blocks

def block_to_block_type(block) -> BlockType:
    
    for i in range(1, 7):
        if block.startswith("#" * i + " "):
            return BlockType.HEADING
        
        
    if block.startswith("```\n") and block.endswith("```"):
     return BlockType.CODE
 
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    is_ordered = True
    expected_number = 1
    for line in lines:
        if not line.startswith(f"{expected_number}. "):
            is_ordered = False
            break
        expected_number += 1
    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH