
from textnode import TextNode, TextType
import os
import shutil

def copy_static(source, destination):
    if os.path.exists(destination):
            shutil.rmtree(destination)
    os.mkdir(destination)
    copy_directory(source, destination)
    
    
def copy_directory(source, destination):
    items = os.listdir(source)

    for item in items:
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




def main():
    node = TextNode("Hello, World!", TextType.TEXT, url="https://example.com")
    print(node)
    copy_static("static", "public")


if __name__ == "__main__":
    main()