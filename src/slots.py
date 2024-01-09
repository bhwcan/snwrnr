# Copyright (c) 2023, bhwcan
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. 

import os
import sys
import glob
import json
import pprint
from datetime import datetime
from datetime import timezone

sys.tracebacklimit = 0

MAPS = {
  'level_us_01_01': ["Black River", "Michigan", "USA"],
  'level_us_01_02': ["Smithville Dam", "Michigan", "USA"],
  'level_us_01_03': ["Island Lake", "Michigan", "USA"],
  'level_us_01_04': ["Drummond Island", "Michigan", "USA"],
  'level_us_02_01': ["North Port", "Alaska", "USA"],
  'level_us_02_02': ["Mountain River", "Alaska", "USA"],
  'level_us_02_03': ["White Valley", "Alaska", "USA"],
  'level_us_02_04': ["Pedro Bay", "Alaska", "USA"],
  'level_ru_02_02': ["Drowned Lands", "Taymyr", "Russian Federation"],
  'level_ru_02_01': ["Quarry", "Taymyr", "Russian Federation"],
  'level_ru_02_03': ["Zimnegorsk", "Taymyr", "Russian Federation"],
  'level_ru_02_04': ["Rift", "Taymyr", "Russian Federation"],
  'level_ru_03_01': ["Lake Kovd", "Kola Peninsula", "Russian Federation"],
  'level_ru_03_02': ["Imandra", "Kola Peninsula", "Russian Federation"],
  'level_us_04_01': ["Flooded Foothills", "Yukon", "Canada"],
  'level_us_04_02': ["Big Salmon Peak", "Yukon", "Canada"],
  'level_us_03_01': ["Black Badger Lake", "Wisconsin", "USA"],
  'level_us_03_02': ["Grainwoods River", "Wisconsin", "USA"],
  'level_ru_04_01': ["Urska River", "Amur", "Russian Federation"],
  'level_ru_04_02': ["Cosmodrome", "Amur", "Russian Federation"],
  'level_ru_04_03': ["Northern Aegis Installation", "Amur", "Russian Federation"],
  'level_ru_04_04': ["Chernokamensk", "Amur", "Russian Federation"],
  'level_ru_05_01': ["Factory Grounds", "Don", "Russian Federation"],
  'level_ru_05_02': ["Antonovskiy Nature Reserve", "Don", "Russian Federation"],
  'level_us_06_01': ["The Lowland", "Maine", "USA"],
  'level_us_06_02': ["Yellowrok National Forest", "Maine", "USA"],
  'level_us_07_01': ["Burning Mill", "Tennessee", "USA"],
  'level_ru_08_01': ["Crossroads", "Belozersk Glads", "Central Asia"],
  'level_ru_08_02': ["The Institue", "Belozersk Glads", "Central Asia"],
  'level_ru_08_03': ["Heartlands", "Belozersk Glads", "Central Asia"],
  'level_ru_08_04': ["HarvestCorp", "Belozersk Glads", "Central Asia"],
  'level_us_09_01': ["The Albany River", "Ontario", "Canada"],
  'level_us_09_02': ["Burned Forest", "Ontario", "Canada"],
  'level_us_10_01': ["Duncan Bay", "British Columbia", "Canada"],
  'level_us_10_02': ["North Peaks National Park", "British Columbia", "Canada"],
  'level_us_11_01': ["Mountain Ridge", "Scandinavia", "Northern Europe"],
  'level_us_11_02': ["By the Lake", "Scandinavia", "Northern Europe"],
  'level_us_12_01': ["Pineline Bay", "North Carolina", "USA"],
  'level_us_12_02': ["Reactive Zone", "North Carolina", "USA"],
  'level_us_12_03': ["Flatland", "North Carolina", "USA"],
  'level_us_12_04': ["Oviro Hills", "North Carolina", "USA"],
}
        
class Slot:
    def __init__(self):
        self.index = None
        self.savename = ""
        self.completesave = ""
        self.d = None
        self.j = None
        self.report = []

class Game:
    def __init__(self):
        self.path = None
        self.slots = [Slot(),Slot(),Slot(),Slot()]
        i = 0
        for slot in self.slots:
            slot.index = i
            i = i + 1

    def open(self, sr_path):
        if not os.path.isdir(sr_path):
            return
        self.path = sr_path
        os.chdir(self.path)
        savenames = ['CompleteSave.dat', 'CompleteSave1.dat', 'CompleteSave2.dat', 'CompleteSave3.dat',
                     'CompleteSave.cfg', 'CompleteSave1.cfg', 'CompleteSave2.cfg', 'CompleteSave3.cfg']


        saves = glob.glob("CompleteSave*")
        #print(saves)

        count = 0
        index = -1
        for name in saves:
            if name not in savenames:
                continue
            
            if name[12] == '.':
                index = 0
            if name[12] == '1':
                index = 1
            if name[12] == '2':
                index = 2
            if name[12] == '3':
                index = 3
            if index < 0 or index > 3:
                continue

            count = count + 1
            self.slots[index].completesave = name
            self.slots[index].savename = name[:-4]
            with open(name, 'r') as jf:
                self.d = jf.read()
                self.slots[index].j = json.loads(self.d[:-1])

        if count < 1:
            raise Exception("no save games found")
        
def usage():
    print("Usage:")
    print("List slots for Snowrunner game.\n")
    print("python slots.py <save1>")

def main():
    argc = len(sys.argv)
    #print(f"Arguments count: {argc}")
    if argc <= 1:
        usage()
        exit(0)

    location = sys.argv[1]
    if not os.path.isdir(location):
        raise Exception("invalid game save location "+location)
    
    game = Game()
    game.open(location)

    if game.path is None:
        print("game not found: ", sr_path)
        exit(1)

    print("game found: ", game.path,"\n")
    for slot in game.slots:
        if slot.index is None:
            continue

        save = None
        if game.slots[slot.index].j:
            save = game.slots[slot.index].j[game.slots[slot.index].savename]['SslValue']

        #print(slot.index, slot.savename)

        startingTruck = "unknown"
        
        if save:
            ds = save.get('gameDifficultySettings')
            if ds:
                startingTruck = ds.get('startingTruck')

        if save and save['lastLoadedLevel']:
            #print(save['lastLoadedLevel'])
            if save['lastLoadedLevel'][:14] in MAPS:
                map = MAPS[save['lastLoadedLevel'][:14]]
            else:
                map = ["Mod Map", save['lastLoadedLevel'], "---"]
        else:
            map = [ "---", "---", "---"]

        timestamp = None
        if save:
            timestamp = float(int(save['saveTime']['timestamp'],16))/1000
        if timestamp:
            dt_object = datetime.fromtimestamp(timestamp,timezone.utc)
            j = dt_object.strftime('%A')
            d = dt_object.strftime('%Y-%m-%d')
            t = dt_object.strftime('%H:%M:%S')
        else:
            j = "---"
            d = "---"
            t = "---"

        hardmode = ""
        rank = "Rank: ***"
        money = "Money: ***"
        experience = "Experience: ***"

        if save:
            if save['isHardMode']:
                hardmode = "Hard Mode"
            elif "gameDifficultyMode" in save and save['gameDifficultyMode'] == 2:
                hardmode = "New Game +"

            if save['persistentProfileData'] and save['persistentProfileData']['rank']:
                rank = "Rank: {rank}".format(rank=save['persistentProfileData']['rank'])

            if save['persistentProfileData'] and save['persistentProfileData']['money']:
                money = "Money: {money}".format(money=save['persistentProfileData']['money'])
 
            if save['persistentProfileData'] and save['persistentProfileData']['experience']:
                experience = "Experience: {exp}".format(exp=save['persistentProfileData']['experience'])
        
        w = 28

        slotnum = "Slot: {num}".format(num=slot.index+1)
        slot.report.append(slotnum.center(w))
        slot.report.append("\033[92m"+("["+startingTruck+"]").center(w)+"\033[0m")
        #slot.report.append(("["+startingTruck+"]").center(w))
        slot.report.append("".center(w))
        slot.report.append(map[0].center(w))
        slot.report.append(map[1].center(w))
        slot.report.append(map[2].center(w))
        slot.report.append("".center(w))
        slot.report.append(j.center(w))
        slot.report.append(d.center(w))
        slot.report.append(t.center(w))
        slot.report.append(hardmode.center(w))
        slot.report.append(rank.center(w))
        slot.report.append(money.center(w))
        slot.report.append(experience.center(w))

    i = 0
    
    for l in game.slots[0].report:
        l1 = game.slots[0].report[i]
        l2 = game.slots[1].report[i]
        l3 = game.slots[2].report[i]
        l4 = game.slots[3].report[i]
        if argc == 3:
             print(l1)
        else:
            print(l1,l2,l3,l4)
        i = i + 1

# MAIN        
if __name__ == "__main__":

    if os.name == 'nt': # Only if we are running on Windows
        from ctypes import windll
        k = windll.kernel32
        k.SetConsoleMode(k.GetStdHandle(-11), 7)    
    
    main()

