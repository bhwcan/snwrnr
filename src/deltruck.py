#!/usr/bin/env python

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

def deleteTruck(save, truck_name, count):

    storage = save.data[save.name]['SslValue']['persistentProfileData']['trucksInWarehouse']

    print(save.filename, "Available Trucks: ", count)
    indexes = []
    i = 0
    for t in storage:
        print("\t", t['type'])
        if truck_name == "all" or t['type'] == truck_name:
            indexes.append(i)
        i += 1

    if truck_name == "":
      return len(storage)

    print("\nDeleting trucks from storage:")
    if len(indexes) > 0:
      for index in sorted(indexes, reverse=True):
        if decOwned(save, storage[index]['type'], count):
          print("deleting:", storage[index]['type'], "at", index)
          del storage[index]
    else:
        exit("ERROR truck not found in " + save.filename)
    
    return len(indexes)

def decOwned(save, key, c):
    count = 0
#    print(save.name)
#    pprint.pprint(save.data)
    owned = save.data[save.name]['SslValue']['persistentProfileData']['ownedTrucks']
    if key in owned:
        count = owned[key]
        print(key, "owned", count)
        if count > c:
          count = count - 1
          owned[key] = count
          #print(key, count, owned[key])
          return True
    return False
    

def writeSaveFile(save):
    f = open(save.filename, "w")
    json.dump(save.data, f, separators=(',', ':'))
    f.write('\00')
    f.close()

def usage():
    print("Usage:")
    print("Delete a truck in storage from one save file.\n")
    print("python deltruck.py <save1> <truck>")
    print("\tno arguments print this message")
    print("\tone save file print available trucks")
    print("\ttwo arguments delete truck from save1\n")
        
# MAIN
if __name__ == "__main__":
  count = 0
  argc = len(sys.argv)
  #print(f"Arguments count: {argc}")
  if argc <= 1:
    usage()
    exit(0)
  fd = openSaveFile(sys.argv[1])
  truck_name = ""
  if argc >= 3:
    truck_name = sys.argv[2]
  if argc >= 4:
    count = int(sys.argv[3])
  deleteTruck(fd, truck_name, count)

  #debug
  #print("\nList after delete:")
  #deleteTruck(fd, "", 0)
    
  writeSaveFile(fd)
    
 

