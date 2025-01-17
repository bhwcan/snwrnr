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
    f = open(filename, 'r', encoding="utf-8", errors='ignore')
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

def findTruck(save, truck_name):

    truck_data = []
    storage = save.data[save.name]['SslValue']['persistentProfileData']['trucksInWarehouse']

    print(save.filename, "Available Trucks: ")
    for i in storage:
      print("\t", i['type'])
      if i['type'] == truck_name:
        truck_data.append(i)

    if truck_name == "":
      exit(0)
      
    if len(truck_data) < 1:
      exit("ERROR truck not found in " + save.filename)

    return truck_data

def addTruck(save, trucks):

  for truck_data in trucks:
    #pprint.pprint(truck_data)
    key = truck_data['type']
    truck_data['retainedMapId'] = ""

    count = incOwned(save, key)

    storage = save.data[save.name]['SslValue']['persistentProfileData']['trucksInWarehouse']
    storage.append(truck_data)

    print("Added truck", key, "at count", count, "to", save.filename)

def incOwned(save, key):
    count = 0
    owned = save.data[save.name]['SslValue']['persistentProfileData']['ownedTrucks']
    if key in owned:
        count = owned[key]
    count = count + 1
    owned[key] = count
    return count
    
def allTrucks(fd, td):

    storage = fd.data[fd.name]['SslValue']['persistentProfileData']['trucksInWarehouse']
    addTruck(td, storage)


def writeSaveFile(save):
    f = open(save.filename, "w", encoding="utf-8")
    json.dump(save.data, f, separators=(',', ':'))
    f.write('\00')
    f.close()

def usage():
    print("Usage:")
    print("Copy truck in storage from one save file to another.\n")
    print("python copytruck.py <save1> <save2> <truck>")
    print("\tno arguments print this message")
    print("\tone save file print available trucks")
    print("\tthree arguments copy truck from save1 to save2\n")
    print("Notes:")
    print("\tyou need to own the DLC for DLC content to show up")
    print("\tif two or more trucks are the same in save1 it will copy all\n")
    print("Example:")
    print("python copytruck.py CompleteSave3.dat CompleteSave.dat gmc_9500\n")
    print("Output:")
    print("CompleteSave3.dat Available Trucks:")
    print("\tstep_3364_crocodile\n\tgmc_9500\n\tvoron_grad\n\tpacific_p16\n\tderry_longhorn_4520\n\tkrs_58_bandit\n\ttuz_420_tatarin")
    print("Added truck gmc_9500 at count 1 to CompleteSave.dat")
        
# MAIN
if __name__ == "__main__":
    argc = len(sys.argv)
    #print(f"Arguments count: {argc}")
    if argc <= 1:
        usage()
        exit(0)
    fd = openSaveFile(sys.argv[1])
    truck_name = ""
    if argc == 4:
        truck_name = sys.argv[3]
    if argc >= 3:
        td = openSaveFile(sys.argv[2])
    if truck_name == "all":
        allTrucks(fd, td)
    else:
        truck_data = findTruck(fd, truck_name)
        addTruck(td, truck_data)
    writeSaveFile(td)
    
 

