from textnode import TextNode, TextType

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    new_blocks = []

    for block in blocks:
        block = block.strip()

        if block != "":
            new_blocks.append(block)

    return new_blocks