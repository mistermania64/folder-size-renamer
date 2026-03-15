# Author: mistermania
# Script Type: Python 3
# Find more at: https://github.com/mistermania64

import os
import re

path = os.getcwd()
files = os.listdir(path)

# Function to calculate the total size (in bytes) of a directory and all its contents, including subdirectories
def get_dir_size(path='.'):

    total_size = 0

    # Use os.scandir() for efficiency as it retrieves file attributes along with names
    with os.scandir(path) as entries:
        for file in entries:
            try:
                # If file, add size in bytes to total
                if file.is_file(follow_symlinks=False):
                    total_size += file.stat(follow_symlinks=False).st_size

                # If folder, call function recursively
                elif file.is_dir(follow_symlinks=False):
                    total_size += get_dir_size(file.path)

            except (FileNotFoundError, PermissionError):
                # Skip files/dirs that can't be accessed (e.g., broken symlinks or permission issues)
                continue
            
    return total_size

for filename in files:
    if os.path.isdir(filename):
        print("Folder: " + filename + ".\n")
        size = get_dir_size(filename)

        # 1 GB = 1073741824 Bytes
        # 1 MB = 1048576 Bytes
        # 1 KB = 1024 Bytes
        
        # If size is less than one kilobyte, display size in bytes (B)
        if size < 1024:
            new_size = size # No conversion necessary
            size_type = " B"

        # If size is less than one megabyte, display size in kilobytes (KB)
        elif size < 1048576: 
            new_size = (size / (1024)) # Convert size to kilobytes
            size_type = " KB"

        # If size is less than one gigabyte, display size in megabytes (MB)
        elif size < 1073741824:
            new_size = (size / (1024**2))  # Convert size to megabytes
            size_type = " MB"      

        # Else, size is at least one gigabyte, display in gigabytes (GB)
        else: # size >= 1073741824: 
            new_size = (size / (1024**3)) # Convert size to gigabytes
            size_type = " GB"
        
        # Skip hidden folders
        if not filename.startswith("$") and not filename.startswith("."):

            # For folders that have already been calculated, replace size instead of appending
            if (filename.endswith("B]")):

                # Match size pattern in string
                old_size = r'\[\d+\.\d+\s[K,M,G]?B\]' 
                
                # Construct filename with new size
                new_size_string = "[" + "{:.1f}".format(new_size) + size_type + "]"
                empty = ""

                # Create string to overwrite old filename
                renamed_string = re.sub(old_size, empty, filename, count=1) 
        
                os.rename(filename, renamed_string)

            else:
                # os.rename(str(filename), str(filename) + " [" + "{:.1f}".format(new_size) + size_type + "]")
                continue
                
    else:
        print("File: " + filename + ".\n")
