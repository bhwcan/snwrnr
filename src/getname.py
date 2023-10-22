import fnmatch
import os
import re
import sys

def find_files(base, pattern):
    index = 0
    first_match = None
    for file in os.listdir(base):
        if fnmatch.fnmatch(file, pattern):
            if not first_match:
                first_match = file
            if file[-1].isdigit():
                m = re.search(r'\d+$', file)
                if int(m.group()) > index:
                    first_match = file
                    index = int(m.group())
    return first_match

# MAIN
if __name__ == "__main__":
    argc = len(sys.argv)
    #print(f"Arguments count: {argc}")
    if argc <= 2:
        print("ERROR")
        exit(1)

    backup = sys.argv[1]
    pattern = sys.argv[2] + "*"
    file = find_files(backup, pattern)
    print(file)