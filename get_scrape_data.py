import os
from subprocess import PIPE, run
import json
import sys

TARGET_NAME = "scrape"

def find_all_scrape_dir(source):
    scrape_paths = []
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if  TARGET_NAME in directory.lower():
                path = os.path.join(source, directory)
                scrape_paths.append(path)
        break
    return scrape_paths

        

def main(source, dest):
    current_dir = os.getcwd()
    source_path = os.path.join(current_dir, source)
    dest_path = os.path.join(current_dir, dest)

    scrape_paths = find_all_scrape_dir(source_path)
    print(scrape_paths)



if __name__ == "__main__":
    args = sys.argv
    
    if len(args) != 3:
        raise Exception("Source and destination directories are expected.")
    
    source, dest = args[1:]
    main(source, dest)


# current_dir = os.getcwd()1
# print(current_dir)





 