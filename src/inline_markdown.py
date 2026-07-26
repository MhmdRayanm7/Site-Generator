import re
from textnode import TextNode, TextType

def extract_markdown_images(text)-> list[tuple] :
     return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text)-> list[tuple] :
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)    

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
        
        new_nodes = [] 
        
        for node in old_nodes:
            
            if node.text_type != TextType.TEXT:
                    new_nodes.append(node)
                    continue
                
            parts = node.text.split(delimiter)
            
            if len(parts) % 2 == 0:
                raise Exception("The text must have a closing delimiter")
            
            for i in range(len(parts)):
                part = parts[i]

                if part == "":
                    continue

                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))

        return new_nodes  
    
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        for alt_text, url in images:
            image_markdown = f"![{alt_text}]({url})"
            parts = remaining_text.split(image_markdown, 1)

            if parts[0] != "":
                new_nodes.append(
                    TextNode(parts[0], TextType.TEXT)
                )

            new_nodes.append(
                TextNode(alt_text, TextType.IMAGE, url)
            )

            remaining_text = parts[1]

        if remaining_text != "":
            new_nodes.append(
                TextNode(remaining_text, TextType.TEXT)
            )

    return new_nodes
        
        

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:         
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_links(node.text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        for alt_text, url in images:
            link_markdown = f"[{alt_text}]({url})"
            parts = remaining_text.split(link_markdown, 1)

            if parts[0] != "":
                new_nodes.append(
                    TextNode(parts[0], TextType.TEXT)
                )

            new_nodes.append(
                TextNode(alt_text, TextType.LINK, url)
            )

            remaining_text = parts[1]

        if remaining_text != "":
            new_nodes.append(
                TextNode(remaining_text, TextType.TEXT)
            )

    return new_nodes

    
def text_to_textnodes(text: str) -> list[TextNode]:
    
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
    