import os
from datetime import datetime

def print_directory_contents():
    print("Directory Contents:")
    print("--------------------------------------")
    print(f"{"\n".join(os.listdir())}")
    print("--------------------------------------")

def print_environment_variables():
    print("Environment Variables:")
    print("--------------------------------------")
    print(f"{"\n".join(os.environ.keys())}")
    print("--------------------------------------")

def create_directories(directories):
    os.makedirs(directories, exist_ok=True)
    os.chdir(directories)

def remove_directories(directories):
    os.chdir(os.path.pardir)
    os.removedirs(directories)

def get_file_info(file):
    size = os.path.getsize(file)
    creation_time = os.path.getctime(file)
    return size, datetime.fromtimestamp(creation_time)

def main():

    print(f"Current working directory: {os.getcwd()}")
    print("--------------------------------------")

    dir_contents = os.listdir()
    print("Directory Contents:")
    print("--------------------------------------")
    # get the file name, size and creation time of each file
    for file in dir_contents:
        size, creation_time = get_file_info(file)
        print(f"File: {file}\t Size: {size}\t Creation Time: {creation_time}")
    print("--------------------------------------")

    # get dirpath, dirnames, and filenames
    dirpath, dirnames, filenames = next(os.walk(os.getcwd()))

    print("Directory Info:")
    print("--------------------------------------")
    print("dirpath:", dirpath)
    print("--------------------------------------")

    print("--------------------------------------")
    print("directories:", dirnames)
    print("--------------------------------------")

    print("--------------------------------------")
    print("files:", filenames)
    print("--------------------------------------")

if __name__ == "__main__":
    main()
