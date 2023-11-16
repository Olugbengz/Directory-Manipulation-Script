import os
from subprocess import PIPE, run
import json
import sys
import shutil 


TARGET_NAME = "scrape"
SCRAPE_NAME_EXTENSION = 'go'
SCRAPE_FILE_COMPILE_COMMAND = ['go', 'build']

def find_all_scrape_dir(source):
    scrape_paths = []
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if  TARGET_NAME in directory.lower():
                path = os.path.join(source, directory)
                scrape_paths.append(path)
        break
    return scrape_paths


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def get_name_from_paths(paths, name_to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(name_to_strip, '')
        new_names.append(new_dir_name)

    return new_names


def run_command(command, path):
    cwd = os.getcwd()
    os.chdir()

    result = run(command, stdout=PIPE, stdin=PIPE,universal_newlines=True)
    print("compiled result: ", result)

    os.chdir(path)


def compile_scrape_code(path):
    code_file_name = None
    for root, dirs, files in path:
        for file in files:
            if SCRAPE_NAME_EXTENSION == 'go':
                code_file_name = file
                break
        break

    if code_file_name == None:
        return
    
    command =  SCRAPE_FILE_COMPILE_COMMAND + [code_file_name]
    run_command(command, path)


def make_json_meta_data_file(path, scrape_dir):
    data = {
        "scrapedFileName": scrape_dir,
        "numberOScrapedFiles": len(scrape_dir)
    }

    with open(path, 'w') as f:
        json.dump(data, f)


def copy_and_overwite_dest(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source, dest)

      

def main(source, dest):
    current_dir = os.getcwd()
    source_path = os.path.join(current_dir, source)
    dest_path = os.path.join(current_dir, dest)

    scrape_paths = find_all_scrape_dir(source_path)
    new_scrape_dirs = get_name_from_paths(scrape_paths, 'scrape')

    create_dir(dest_path)

    for src, dest in zip(scrape_paths, new_scrape_dirs):
        target_path = os.path.join(dest_path, dest)
        copy_and_overwite_dest(src, target_path)
        compile_scrape_code(target_path)

    json_path = os.path.join(dest_path)
    make_json_meta_data_file(json_path, new_scrape_dirs)

 
if __name__ == "__main__":
    args = sys.argv
    
    if len(args) != 3:
        raise Exception("Source and destination directories are expected.")
    
    source, dest = args[1:]
    main(source, dest)


# current_dir = os.getcwd()1
# print(current_dir)





    