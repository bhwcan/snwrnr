import fnmatch
import os
import re
import sys

backup = "L:\\Snowrunner\\backup"

def find_files(base, pattern):
    first_match = None
    index = 0
    for file in os.listdir(base):
        if fnmatch.fnmatch(file, pattern):
            if not first_match:
                first_match = file
            if file[-1].isdigit():
                m = re.search(r'\d+$', file)
                if int(m.group()) > index:
                    first_match = file[0:m.span()[0]]
                    index = int(m.group())
    if not first_match:
        first_match = pattern[0:-1]
    if (first_match[-1] not in " -_"):
        first_match += "-"
    #print(first_match, index)  
    return first_match + "{index:04d}".format(index=index+1)
    #'''Return list of files matching pattern in base folder.'''
    #return [n for n in fnmatch.filter(os.listdir(base), pattern) if
    #    os.path.isfile(os.path.join(base, n))]

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