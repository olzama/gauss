import os, sys, glob, re

# Code created by ChatGPT and adapted to the following path structure: path-to-folders/test/long/cow10-test/item
def process_directory(directory_path):
    filename = "item"
    folders = glob.iglob(directory_path + '/**/**/')
    for fol in folders:
        filepath = os.path.join(fol, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as f:
                lines = f.readlines()
            with open(filepath, 'w') as f:
                for line in lines:
                    new_line = re.sub(r'((?:[^@]*@){7})[^@]*(@)', r'\1\2', line)
                    f.write(new_line)
            print(f"Processed file: {filepath}")
if __name__ == '__main__':
    directory_path = sys.argv[1] # Expected input: /path-to-folder/test/
    process_directory(directory_path)
