from textnode import TextNode, TextType , text_node_to_html_node 
from inline_markdown import text_to_textnodes
from enum import Enum
from htmlnode import HTMLNode , ParentNode , LeafNode


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


def text_to_children(text : str)-> list[HTMLNode] :
    text_nodes = text_to_textnodes(text)
    children = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)

    return children

def block_to_html_node(block):
    t = block_to_block_type(block)

    if t == BlockType.PARAGRAPH:
        text = block.replace("\n", " ")
        return ParentNode("p", text_to_children(text))

    elif t == BlockType.HEADING:
        level = 0
        
        while level < len(block) and block[level] == "#":
            level += 1


        text = block[level + 1:]
        return ParentNode(f"h{level}", text_to_children(text))
    
    elif t == BlockType.CODE:
        # Remove opening ```\n and closing ```
        text = block[4:-3]

        text_node = TextNode(text, TextType.TEXT)
        html_node = text_node_to_html_node(text_node)

        code_node = ParentNode("code", [html_node])
        return ParentNode("pre", [code_node])

    elif t == BlockType.QUOTE:
        lines = block.split("\n")
        clean_lines = []

        for line in lines:
            clean_lines.append(line[1:].strip())

        text = " ".join(clean_lines)
        return ParentNode("blockquote", text_to_children(text))

    elif t == BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        list_items = []

        for line in lines:
            text = line[2:]
            list_items.append(
                ParentNode("li", text_to_children(text))
            )

        return ParentNode("ul", list_items)

    elif t == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        list_items = []

        for line in lines:
            text = line.split(". ", 1)[1]
            list_items.append(
                ParentNode("li", text_to_children(text))
            )

        return ParentNode("ol", list_items)

    raise ValueError("Invalid block type")


def markdown_to_html_node(markdown):
    mrk = markdown_to_blocks(markdown)
    children = []
    
    for m in mrk :
        tn = block_to_html_node(m)
        children.append(tn)
        
    return ParentNode("div", children)

def extract_title(markdown) :
    lines = markdown.split("\n")
    
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
        
    raise Exception("No Head Found !")

