import os
import re
import sys
from pathlib import Path
from typing import Optional, Match
import shutil

# Ask user for directory to organize

def get_directory() -> str:
    # Ask for input until user enter correct directory or q
    directory: str = input("Enter a directory to organize its files or q to exit: ")
    while not os.path.exists(directory):
        directory = input("Directory not found! Enter a directory to organize its files or enter q to exit: ")
    # Quit on entering q (Case-insensitive)
    if directory in ["q", "Q"]:
        print("OK, Thank You")
        sys.exit(0)
    # Set entered directory as working directory
    os.chdir(directory)
    print(f"System landed in {directory}") # Notify user
    return directory

# List the files in the directory

def get_list_of_files(directory: str) -> list[str]:
    # Reserve empty list to store the list of file paths
    file_list: list[str] = []
    # Change current directory to Path object to work with pathlib utilities
    directory_path: Path = Path(directory)
    # Iterate the directory: Path using pathlib module iterdir()
    for item in directory_path.iterdir():
         if item.is_file():
              print(f"Tracked: {item}") # Notify user
              file_list.append(str(item))
    return file_list

# Create folders to reserve files based on extension

def reserve_folders(file_list: list[str]) -> list[dict]:
    # Reserve an empty list to store dictionaries {folder:?, file:?} pairs
    reserved_folders: list[dict] = []
    for file in file_list:
        # Set folder names from files extensions
        extension: Optional[Match] = re.match(r"^.+\.([A-Za-z0-9]+)$", file)
        if extension != None:
            folder_name = extension.group(1).upper()
        else:
            folder_name = "NO EXTENSIONS"
        # Create folders if not already exists
        if not os.path.exists(os.path.join(os.getcwd(),folder_name)):
            os.mkdir(folder_name)
            print(f"Folder created: ", folder_name) # Notify User
        else:
            print(f"Folder already exists: ", folder_name) # Notify User
        # Store the dictionaries of folder-file pairs to list
        reserved_folders.append({"folder": folder_name, "file": file})            
    return reserved_folders

# Move files to respective folders

def move_files(reserved_folders: dict) -> None:
    for reserved_pair in reserved_folders:
        # Set source file path and destination path
        source_file = reserved_pair["file"] # get source file path from stored list of dictionaries
        file_name = os.path.basename(source_file) # extract file name from path string
        destination_folder = os.path.join(os.getcwd(),reserved_pair["folder"]) # set destination folder path
        destination_file = os.path.join(destination_folder, file_name) # set destination file path by joining folder and file name
        try:
            # Move file
            shutil.move(source_file, destination_file)
            print(f"Moved: {source_file} to {destination_file}") # Notify user
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