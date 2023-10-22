# Python program to copy snowrunner truck
import json
import pprint
import sys

class Save:
    def __init__(self):
        self.filename = ""
        self.name = ""
        self.data = {}
        
def openSaveFile(filename):

    #print(filename)
    
    # JSON file
    f = open(filename)
    rd = f.read()
    #print(rd[-1], rd[-10:])
    if rd[-1] == '\x00':
        data = json.loads(rd[:-1])
    else:
        data = json.loads(rd)
    f.close()

    save = Save()

    for name in data:
        if name[:12] == "CompleteSave":
            save.name = name

    if save.name == "":
        exit("ERROR Invalid save file: " + filename)

    save.filename = filename
    save.data = data
    return save

def setTruck(save, struck):

    save.data[save.name]['SslValue']['gameDifficultySettings']['startingTruck'] = struck


def writeSaveFile(save):
    f = open(save.filename, "w")
    json.dump(save.data, f, separators=(',', ':'))
    f.write('\00')
    f.close()


def usage():
    print("Usage:")
    print("Set starting truck in save file.\n")
    print("python settruck.py <save1> <truck>")
    print("\tno arguments print this message")
        
# MAIN
if __name__ == "__main__":
    argc = len(sys.argv)
    #print(f"Arguments count: {argc}")
    if argc <= 1:
        usage()
        exit(0)
    fd = openSaveFile(sys.argv[1])
    print("name:", fd.data[fd.name]['SslValue']['gameDifficultySettings']['startingTruck'])
    if argc > 2:
        print("  to:", sys.argv[2])
        setTruck(fd, sys.argv[2])
        writeSaveFile(fd)
#    truck_name = ""
#    if argc == 4:
#        truck_name = sys.argv[3]
#    truck_data = findTruck(fd, truck_name)
#    td = openSaveFile(sys.argv[2])
#    addTruck(td, truck_data)
    
 

