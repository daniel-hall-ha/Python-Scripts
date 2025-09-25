import os
import re
import sys
from pathlib import Path
from typing import Optional, Match
import shutil

def get_directory() -> str:
    directory: str = input("Enter a directory to organize its files or q to exit: ")
    while not os.path.exists(directory):
        directory = input("Directory not found! Enter a directory to organize its files or enter q to exit: ")
    if directory in ["q", "Q"]:
        print("OK, Thank You")
        sys.exit(0)
    os.chdir(directory)
    print(f"System landed in {directory}")
    return directory

def get_list_of_files(directory: str) -> list[str]:
    file_list: list[str] = []
    directory_path: Path = Path(directory)
    for item in directory_path.iterdir():
         if item.is_file():
              print(f"Added: {item}")
              file_list.append(str(item))
    return file_list

def reserve_folders(file_list: list[str]) -> list[dict]:
    reserved_folders: list[dict] = []
    for file in file_list:

        extension: Optional[Match] = re.match(r"^.+\.([A-Za-z0-9]+)$", file)
        if extension != None:
            folder_name = extension.group(1).upper()
        else:
            folder_name = "NO EXTENSIONS"

        if not os.path.exists(os.path.join(os.getcwd(),folder_name)):
            os.mkdir(folder_name)
            print(f"Folder created: ", folder_name)
        else:
            print(f"Folder already exists: ", folder_name)    
        
        reserved_folders.append({"folder": folder_name, "file": file})        
    
    return reserved_folders

def move_files(reserved_folders: dict) -> None:
    for reserved_pair in reserved_folders:
        source_file = reserved_pair["file"]
        file_name = os.path.basename(source_file)
        destination_folder = os.path.join(os.getcwd(),reserved_pair["folder"])
        destination_file = os.path.join(destination_folder, file_name)
        try:
            shutil.move(source_file, destination_file)
            print(f"Moved: {source_file} to {destination_file}")
        except FileNotFoundError:
            print("File not found!")
        except shutil.Error as e:
            print(f"An error occured {e}")

def main():
    working_directory = get_directory()
    list_of_files = get_list_of_files(working_directory)   
    reserved_folders = reserve_folders(list_of_files)
    move_files(reserved_folders)

if __name__ == "__main__":
    main()