
from textnode import TextNode, TextType
from block_markdown import markdown_to_html_node , extract_title
import os
import shutil
import sys

def copy_static(source, destination):
    if os.path.exists(destination):
            shutil.rmtree(destination)
    os.mkdir(destination)
    copy_directory(source, destination)
    
    
def copy_directory(source, destination):
    items = os.listdir(source)

    for item in items:
        # Build the full destination , s path for the current item
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        
        if os.path.isfile(source_path):
            print("File")
            shutil.copy(source_path,destination_path)
            
        else:
            print("Directory")
            os.mkdir(destination_path)
            copy_directory(source_path,destination_path)

        print(f"Source: {source_path}")
        print(f"Destination: {destination_path}")

def generate_page(from_path, template_path, dest_path, basepath):
    print(
    f"Generating page from {from_path} "
    f"to {dest_path} using {template_path}")
    
    with open(from_path, "r", encoding="utf-8") as file:
        markdown = file.read()

    with open(template_path, "r", encoding="utf-8") as temp:
        template = temp.read()
        
    html = markdown_to_html_node(markdown) 
    html_content = html.to_html()
    title = extract_title(markdown)

    full_page = template.replace("{{ Title }}", title)
    full_page = full_page.replace("{{ Content }}", html_content)
    full_page = full_page.replace('href="/' , f'href="{basepath}')
    full_page = full_page.replace('src="/', f'src="{basepath}')
    
    name = os.path.dirname(dest_path)

    if name != "":
        os.makedirs(name, exist_ok=True)
        
    with open(dest_path, "w", encoding="utf-8") as file:
        dest_path = file.write(full_page)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path , basepath):
    en = os.listdir(dir_path_content)

    for e in en:
        content_path = os.path.join(dir_path_content, e)
        destination_path = os.path.join(dest_dir_path, e)

        if os.path.isdir(content_path):
            generate_pages_recursive(
                content_path,
                template_path,
                destination_path,
                basepath,
            )

        elif e.endswith(".md"):
            html_name = os.path.splitext(e)[0] + ".html"
            html_path = os.path.join(dest_dir_path, html_name)

            generate_page(content_path ,template_path ,html_path ,basepath)               

def main():
    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print(basepath)

    copy_static("static", "docs")

    generate_pages_recursive(
    "content",
    "template.html",
    "docs",
    basepath,
    )

if __name__ == "__main__":
    main()