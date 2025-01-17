import os
import sys
import shutil
#from pathlib import Path

BACKUPPATH="/mnt/h/SnowRunner/work/backup"
#READPATH="/mnt/h/SnowRunner/work/a6b8b8cca2ea4c8586f9550081030d21"
READPATH="/mnt/h/SnowRunner/work/remote"
SLOT=2
NAME="Byron Walton"
STEAM=False

def slotToPrefix(slot):
    prefix = ""
    if slot == "2":
        prefix = "1_"
    if slot == "3":
        prefix = "2_"
    if slot == "4":
        prefix = "3_"

    return prefix

def slotToSuffix(slot):
    suffix = ""
    if slot == "2":
        suffix = "1"
    if slot == "3":
        suffix = "2"
    if slot == "4":
        suffix = "3"

    return suffix

def saveExtension():
    global STEAM
    if STEAM:
        ext = ".cfg"
    else:
        ext = ".dat"
    return ext

def createBackupDir(backup, name):

    if not os.path.exists(backup):
        raise Exception( "missing backup dir or save backup doesn't exist" )

    if not os.path.isdir(backup):
        raise Exception( "backup is not a directory")
    
    bdir = backup + os.path.sep + name
    print(bdir)
    if os.path.exists(bdir):
        raise Exception( "backup name already exists" )
    os.makedirs(bdir, exist_ok=False)
    print("Backup to", bdir)
    return bdir

def copyCompleteSaveFile(save, slot, backup):
    global STEAM
    print(save, slot)

    if save[-6:] == 'remote':
        STEAM = True

    filename = save + os.path.sep + "CompleteSave" + slotToSuffix(slot) + saveExtension()
    backupname = backup + os.path.sep + "CompleteSave.dat"
    
    if os.path.exists(filename):
        raise Exception( "restore to existing slot" )
    if not os.path.exists(backupname):
        raise Exception( "missing backup dir or backup dir doesn't exist" )
    
    fr = open(backupname, "r", encoding="utf-8", errors='ignore')
    rd = fr.read()
    wd = rd.replace("CompleteSave", "CompleteSave" + slotToSuffix(slot))
    fr.close()

    #print(filename, wd[:40])
    #exit(1)
    
    fw = open(filename, "w+", encoding="utf-8")
    fw.write(wd)
    fw.close()

def copyFiles(save, slot, backup):

    for f in os.listdir(backup):
        if f.startswith("sts") or \
           f.startswith("fog"):
            new = slotToPrefix(slot) + f[:-4] + saveExtension()
            print(os.path.join(backup, f), "->", os.path.join(save, new))
            shutil.copyfile(os.path.join(backup, f), os.path.join(save, new))
    
def usage():
    print("Usage:")
    print("Restore Snowrunner Save Slot.\n")
    print("python restoreslot.py <savedir> <backupdir> <slot> <name>")
    print("\tno arguments print this message")

# MAIN
if __name__ == "__main__":
    argc = len(sys.argv)
    #print(f"Arguments count: {argc}")
    if argc <= 1 or argc > 5:
        usage()
        exit(0)
    savedir = sys.argv[1]
    backupdir = sys.argv[2]
    slot = sys.argv[3]
    name = sys.argv[4]
    backup = os.path.join(backupdir, name)
    copyCompleteSaveFile(savedir, slot, backup)
    copyFiles(savedir, slot, backup)
