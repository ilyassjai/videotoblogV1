import os
 
def list_files_and_directories(root_dir='.'):
    file_sizes = []

    for path, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(path, file)
            size = os.path.getsize(file_path)
            file_sizes.append((file_path, size))

    sorted_file_sizes = sorted(file_sizes, key=lambda x: x[1], reverse=True)

    for file_path, size in sorted_file_sizes:
        print(f"{file_path}  ({size} bytes)")

if __name__ == '__main__':
    list_files_and_directories()