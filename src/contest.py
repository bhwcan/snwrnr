#!/usr/bin/env python

import json
import pprint
import sys
from pathlib import Path

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

def writeSaveFile(save):
    f = open(save.filename, "w")
    json.dump(save.data, f, separators=(',', ':'))
    f.write('\00')
    f.close()

class Strings:
    def __init__(self):
        self.filename = ""
        self.data = {}

    def load(self, filename):
        self.filename = filename
        print("strings", filename)
        f = open(filename, "rb")
        d = f.read()
        s = d[2:].decode('utf-16')
        ls = s.splitlines()
        c = 0
        for l in ls:
            d = l[:-1].split("\"",1)
            #print(d[0].strip().upper(),":",d[1])
            self.data[d[0].strip().upper()] = d[1]
            c += 1
            #if c > 10:
            #  pprint.pprint(self.data)
            #  exit(1)
        f.close()
        return c

CONTESTS = {
  "RU_02_01_FIREWATCH_SUPPLY_CNT": [119,3300,430], # "Firewatch Tower Supply"
  "RU_02_01_SERVHUB_FUEL_RESTOCK_CNT": [479,5850,690], # "Fuel Restock"
  "RU_02_01_SHIP_REPAIRS_CNT": [419,3750,450], # "Shipwreck"
  "RU_02_02_BARRELS_DELIVERY_CNT": [479,5500,530], # "Barrels Delivery" 
  "RU_02_02_CONTAINER_DELIVERY_CNT": [479,5600,540], # "Container Delivery"
  "RU_02_02_FLAG_1_CNT": [329,3150,180], # "Rocking And Rolling"
  "RU_02_02_FLAG_2_CNT": [359,2950,170], # "Swimming And Sinking"
  "RU_02_03_CONTEST_BARRELS_DELIVERY_OBJ": [329,6100,990], # "Cement Delivery"
  "RU_02_03_CONTEST_METAL_DELIVERY_OBJ": [479,7400,1070], # "Oilfield Delivery"
  "RU_02_03_CONTEST_WOODEN_DELIVEY_PIRS_OBJ": [269,3750,380], # "Pier Delivery"
  "RU_02_03_CONTEST_WOODEN_DELIVEY_WAREHOUSE_OBJ": [509,3250,350], # "Warehouse Delivery"
  "RU_02_04_RIFT_MAPPING_CNT": [359,3000,180], # "Landslide Mapping"
  "RU_03_01_NORTH_RIVER_RACE_CNT": [239,4350,250], # Battle on the Ice
  "RU_03_01_OFF_THE_RAILS_CNT": [299,4000,230], # Overturned Train Carrage
  "RU_03_02_GARBAGE_CNT": [239,5700,780], # Dirty Business
  "RU_04_01_ICE_RACE_CNT": [214,4450,260], # Ice Adventure
  "RU_04_01_ROCK_RACE_CNT": [389,6100,350], # Conquering Summits
  "RU_04_02_FUEL_RESTOCK_TARGET_CNT": [329,7600,920], # Belated Delivery
  "RU_04_02_FUEL_RUN_CNT": [234,9150,530], # Fuel-Eight
  "RU_04_03_OFF_ROAD": [419,4750,270], # Five Roads Island
  "RU_04_03_RUN": [479,5700,330], # Cliff Sufer
  "RU_04_04__RACE_B_CNT": [519,5200,300], # Endurance Run
  "RU_04_04__RACE_C_CNT": [814,6150,360], # Round and Round
  "RU_04_04__RACE_D_CNT": [239,3550,210], # Street Race
  "RU_04_04_RACE_A_CNT": [284,4750,270], # Highland King
  "RU_05_01_FACTORY_RACE": [59,800,300], # Driving Exam
  "RU_05_01_SWAMP_RACE": [149,1800,180], # Lord of the Frogs
  "RU_05_02_HONEY": [239,2100,460], # Sweet Tooth
  "RU_05_02_LAKE_RACE": [329,3200,650], # The Quick and the Wet
  "US_01_01_FOOD_DELIVERY_CNT": [359,3700,340], # "Food Delivery"
  "US_01_01_METEO_DATA_CNT": [629,3800,220], # "Meteorology Data"
  "US_01_01_WOODEN_ORDER_CNT": [479,3300,360], # "Pinewood Express"
  "US_01_02_FARMERS_NEEDS_CNT": [269,3050,370], # "Heavy Burden"
  "US_01_02_FLOODED_HOUSE_CNT": [479,4350,510], # "Going Under"
  "US_01_02_HOUSE_RENOVATION_CNT": [569,3750,390], # "New Nest"
  "US_01_03_BARREL_CNT": [599,3350,370], # "Flaming Barrels"
  "US_01_04_EXPLORING_CNT": [89,2100,120], # "A Race With The Rain"
  "US_02_01_EMPLOYEE_DISLOCATION_CNT": [419,3250,300], # "Employee Dislocation"
  "US_02_01_FLAGS_CNT": [509,1550,90], # "Race Down To Flags"
  "US_02_01_MOUNTAIN_CONQUEST_1_CNT": [659,2700,160], # "North Mountain Conquest"
  "US_02_01_MOUNTAIN_CONQUEST_2_CNT": [479,2150,130], # "West Mountain Conquest"
  "US_02_02_RIVER_CONTEST_CNT": [199,1700,100], # "River Contest"
  "US_02_02_TO_THE_TOWER_CNT": [129,2650,150], # "To The Top And Back"
  "US_02_03_WEATHER_FORECAST_CNT": [419,6950,1070], # "Weather Forecast"
  "US_02_04_FRAGILE_DELIVERY_CNT": [419,5650,490], # "Weather Conditions"
  "US_03_01_CONT_01": [149,4650,270], # Quarry Race
  "US_03_01_CONT_02": [269,3450,200], # Cliffhanger Race
  "US_03_02_MUDSTER_CNT": [179,8850,510], # Mud Tested
  "US_03_02_SLALOM_CNT": [219,8750,500], # Slalom
  "US_04_01_DOWNHILL_01_CNT": [94,2400,140], # Down!
  "US_04_01_RACE_L_CNT": [209,5100,290], # Long Ride
  "US_04_01_RACE_S_CNT": [119,3200,190], # Short Ride
  "US_04_02_DIRT_CNT": [419,9700,560], # Path through the Rocks
  "US_04_02_TOTHETOP_CNT": [439,4300,250], # To the Top
  "US_06_01_CON_01": [179,4200,240], # Local Racing
  "US_06_01_CON_02": [319,5050,290], # Port-side Racing
  "US_06_02_DANGERRACE_CNT": [269,3150,180], # Dangerous Games
  "US_06_02_KARTER_CNT": [1079,4650,270], # Mysterious Monoliths
  "US_07_01_EXTREME_SLOPE_SOLO": [179,1800,400], #"Extreme Climb",
  "US_07_01_EXTREME_DESCENT_01": [89,900,200], #"Extreme Downhill (CO-OP)",
  "US_07_01_EXTREME_DESCENT_START_SOLO": [89,900,180], #"Extreme Downhill (SOLO)"
  "US_07_01_CIRCUIT_RACE": [359,3600,740], #"The Ring (CO-OP)",
  "US_07_01_QUALIFICATION": [299,3000,600], #"Qualification (CO-OP)",
  "US_07_01_QUALIFICATION_01_START_SOLO": [359,3500,350], #"Qualification (SOLO)"
  "US_07_01_PARKOUR": [59,600,200], #"Paukour",
  "US_07_01_WORKOUT": [9,100,30], #"Gearswitch Training",
  "US_07_01_RACE_START_SOLO": [119,1500,360], #"The Ring (SOLO)"
  "RU_08_04_RING": [259,2200,520], #"Crop Circle"
  "RU_08_04_CONTEST": [299,2800,600], #"Treading Water"
  "RU_08_03_URGENT_DELIVERY_CARGO": [349,4500,350], #"Special Delivery"
  "RU_08_03_FIELDS_RACING": [149,375,375], #"Aim To Misbehave"
  "RU_08_01_LOCAL_FUN": [199,500,500], #"Local Rally"
  "RU_08_01_LAKE_RACE": [239,560,560], #"Lakeside Racing"
  "RU_08_02_SWAMP_RACE": [179,1650,260], #"Swamp Racer"
  "RU_08_02_DOWNHILL_RACE": [29,1500,500], #"Barvery Is A Virtue"
  "RU_08_02_DANGEROUS_DELIVERY": [224,2300,260], #"This Side Up"
  "US_09_01_BARRELS_EXPRESS_DELIVERY_CONTEST": [699,4500,480], # Express fuel delivery
  "US_09_02_MOUNTAIN_TOURISM_CONTEST": [344,3000,320], # Mountain Ride
  "US_10_01_CONTEST_RACE": [299,3250,200], # "Deadly Race"
  "US_10_01_CONT_VISIT": [324,4500,250], # "Data For The Observatory"
  "US_10_02_CONT_01": [159,3700,250], # "All For The Great View!"
  "US_10_02_CONT_02": [299,7200,1000], # "Waste Disposal"
  "US_11_01_FLOODED_RACE_CONTEST": [299,3000,500], # "A Flooded Race"
  "US_11_02_DESCENT_CONTEST": [79,1000,300], # "Challenging Descent"
  "US_11_02_DELIVERY": [299,3000,500], # "Speedy Delivery"
  "US_12_01_TRIAL": [249,2700,500], # Old Road
  "US_12_01_DELIVERY": [209,2200,400], # Litterally on a Timer
  "US_12_02_MUD_TRACK_CONTEST": [179,3200,330], # Swamp Rally
  "US_12_02_MOUNTAIN_RIDE_CONTEST": [179,3000,300], # Secret Place
  "US_12_03_CONT_RACE_01": [99,1800,140], # "What is it"
  "US_12_03_CONT_RACE_02": [114,1800,130], # "Hardships along the way"
  "US_12_04_COASTLINE_RACE_CONTEST": [209,1500,750], # Fast as a Jet
  "RU_13_01_IN_SEARCH_OF_AIDAHAR_CONTEST": [239,1500,750], # In Search of the Aidakhar
  "RU_13_01_MOUNTAIN_CLIMBING_CONTEST": [179,1200,600], # Gone in 240 Seconds
  "US_14_01_URGENT_PHOTOS_CONTEST": [279,2600,150], # Emergency Photo Shoot
  "US_14_01_CITY_RACING_CONTEST": [229,2450,140], # Street Race
  "US_14_02_RACING_CONTEST": [364,4800,300], # Hot Wheels
  "US_14_02_DELIVERY_CONTEST": [359,3400,370], # The Beaver Thieves Strike Again
  "US_15_01_CONTEST_01": [214,3700,220], # Don't Look Up
  "US_15_01_CONTEST_02": [359,11500,1320], # Worth its Weight in Gold
  "US_15_02_CONTEST_RACING": [399,2500,150], # Keep Your Cool on Thin Ice
  "US_15_02_CONTEST_MOUNTAIN": [539,3100,180], # Mountain Trail  
}

MAPS = {}

def build_maps(strings):
    global MAPS

    print("build_maps")
    
    ru = "RU"
    us = "US"
    for i in range(1,16):
      us_s = "{region}_{season:02d}".format(region=us,season=i)
      ru_s = "{region}_{season:02d}".format(region=ru,season=i)
      if us_s in strings.data:
        print(us_s, strings.data[us_s])
        MAPS[us_s.lower()] = strings.data[us_s]
        name = us_s+"_{map:02d}_NAME"
        newname = us_s+"_{map:02d}_NEW_NAME"
        level = "LEVEL_"+name
        levelnoname = "LEVEL_"+us_s+"_{map:02d}"
        for i in range(1, 5):
          found = False
          sname = name.format(map=i)
          slevel = level.format(map=i)
          snewname = newname.format(map=i)
          slevelnoname = levelnoname.format(map=i)
          #print(i, sname, slevel, snewname)
          if sname in strings.data:
            print("\t\'"+slevel+"\': [\""+strings.data[sname]+"\", \""+strings.data[us_s]+"\"],")
            found = True
          elif slevel in strings.data:
            print("\t\'"+slevel+"\': [\""+strings.data[slevel]+"\", \""+strings.data[us_s]+"\"],")
            found = True
          elif snewname in strings.data:
            print("\t\'"+slevel+"\': [\""+strings.data[snewname]+"\", \""+strings.data[us_s]+"\"],")
            found = True
          elif slevelnoname in strings.data:
            print("\t\'"+slevel+"\': [\""+strings.data[slevelnoname]+"\", \""+strings.data[us_s]+"\"],")
            found = True
          if found == False:
            break

      if ru_s in strings.data:
        print(ru_s, strings.data[ru_s])
        MAPS[ru_s.lower()] = strings.data[ru_s]
        name = ru_s+"_{map:02d}_NAME"
        level = "LEVEL_"+name
        for i in range(1, 5):
          found = False
          sname = name.format(map=i)
          slevel = level.format(map=i)
          if sname in strings.data:
            print("\t\'"+slevel+"\': [\""+strings.data[sname]+"\", \""+strings.data[ru_s]+"\"],")
            found = True
          elif slevel in strings.data:
            print("\t\'"+slevel+"\': [\""+strings.data[slevel]+"\", \""+strings.data[ru_s]+"\"],")
            found = True
          if found == False:
            break
  
def usage(strings):
    print("Usage:")
    print("python context.py <savefile> <region>")

    cmap = "XX_XX"
    for c in sorted(CONTESTS.items(), key=lambda x: x[0][3:5]+x[0][0:2]):
      map = c[0][0:5]
      if map != cmap:
        cmap = map
        print("\n", "[", map.lower(), "]", strings.data[map])
      c_id = "** UNKNOWN **"
      if c[0] in strings.data:
        c_id = strings.data[c[0]]
      print("\t", c[0], "\""+c_id+"\"", "[", CONTESTS[c[0]], "]")
          

    # MAIN
if __name__ == "__main__":
    argc = len(sys.argv)
    #print(f"Arguments count: {argc}")
    
    str_file = Path(Path(__file__).resolve().parent, "strings_english.str")
    if not (str_file.exists() and str_file.is_file()):
      print("No strings file found.", str_file)
      exit(10)
      
    strings = Strings()
    strings.load(str_file)
    build_maps(strings)
    
    if argc <= 1:
        usage(strings)
        exit(0)
    fd = openSaveFile(sys.argv[1])

    if argc != 3:
        raise Exception( "Invalid number of arguments" )
    
    LEVEL = sys.argv[2]
    llevel = "level_" + LEVEL
    ulevel = LEVEL.upper()
    HARD = False
    maxattempts = 3

    print("\n--------------------")
    print(ulevel, strings.data[ulevel])
    
    times = fd.data[fd.name]['SslValue']['persistentProfileData']['contestTimes']
    #pprint.pprint(times)
    #exit(10)

    attempts = None

    if(fd.data[fd.name]['SslValue']['persistentProfileData']['contestAttempts']):
        HARD = True
        attempts = fd.data[fd.name]['SslValue']['persistentProfileData']['contestAttempts']
        #pprint.pprint(attempts)
        if 'gameDifficultySettings' in fd.data[fd.name]['SslValue']['persistentProfileData']:
          maxattemps = fd.data[fd.name]['SslValue']['persistentProfileData']['gameDifficultySettings']['maxContestAttempts']
        print("attemps counted to maxium of", maxattempts)
    else:
        print("attempts not counted")
        
    found = False
    total_money = 0
    total_exp = 0
    for t_id, t_info in CONTESTS.items():
        if t_id.startswith(ulevel):
            found = True
            modified = False
            
            print("\n",t_id, "\""+strings.data[t_id]+"\"", t_info[0])
            if t_id in times:
                #print(times[t_id], t_info[0])
                if times[t_id] <= t_info[0]:
                    print("\t", t_id + " time not changed from "+str(times[t_id]))
                else:
                    print("\t", t_id + " time changed from "+str(times[t_id])+" to "+str(t_info[0]))
                    times[t_id] = t_info[0]
                    modified = True
            else:
                times[t_id] = t_info[0]
                print("\t", t_id+" time added "+str(t_info[0]))
                modified = True
                #pprint.pprint(fd.data[fd.name]['SslValue']['finishedObjs'])
                #exit(20)

            if modified:
              
                pd = fd.data[fd.name]['SslValue']['persistentProfileData']
                pd['money'] += t_info[1]
                print("\t", t_id+" money added "+str(t_info[1]))
                total_money += t_info[1]
                pd['experience'] += t_info[2]
                print("\t", t_id+" experience added "+str(t_info[2]))
                total_exp += t_info[2]
                
                finished = fd.data[fd.name]['SslValue']['finishedObjs']
                if t_id not in finished:
                  finished.append(t_id)
                  print("\t", t_id, "added to finished")
                discovered = fd.data[fd.name]['SslValue']['discoveredObjectives']
                if t_id not in discovered:
                  discovered.append(t_id)
                  print("\t", t_id, "added to discovered")
                
                if HARD:
                  count = 0
                  ncount = 0
                  if t_id in attempts:
                    count = attempts[t_id]
                    ncount = count
                  if count < maxattempts:
                    ncount = count + 1
                  print("\t", t_id, "attempts from", count, "set to", ncount)
                  attempts[t_id] = ncount

    #pprint.pprint(times)
    for t_id in times:
        #print("Contest "+ t_id + ":" + str(times[t_id]))
        if t_id not in CONTESTS:
            print("New Contest "+ t_id + ":" + str(times[t_id]))

    if not found:
        print( LEVEL + ": rcegion has no contest data" )
        
    #pprint.pprint(attempts)

    writeSaveFile(fd)

    print("\nContest all gold for", MAPS[LEVEL], "Money added", total_money, "Experience added", total_exp)
