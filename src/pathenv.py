import os
import winreg

regdir = "Environment"
keyname = "Path"
keyvalue = ""

def setRegistry(regdir, keyname, keyvalue):
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, regdir) as _:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, regdir, 0, winreg.KEY_WRITE) as writeRegistryDir:
            winreg.SetValueEx(writeRegistryDir, keyname, 0, winreg.REG_SZ, keyvalue)

def getRegistry(regdir, keyname):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, regdir) as accessRegistryDir:
        value, _ = winreg.QueryValueEx(accessRegistryDir, keyname)
        return(value)

def setPath(path):
    keyvalue = ";".join(path)
    print(keyvalue)
    keyvalue += ";"
    setRegistry(regdir, keyname, keyvalue)

def getPath():
    keyvalue = getRegistry(regdir, keyname)
    print(keyvalue)
    if keyvalue[-1] == ';':
        keyvalue = keyvalue[0:-1]
    return keyvalue.split(';')

def printPath(path):
    c = 1
    print("\nUser Path for", os.environ.get("USERNAME"), "\n")
    for d in path:
        print("{:3d}".format(c), '- ', d)
        c += 1
    print("\n")    

def command(path, cmd, row):

    if cmd == 'a':
        entry = input("Enter new entry: ")
        if os.path.isdir(entry):
            path.append(entry)
        else:
            print("invalid diretory")
    if cmd == 'd':
        path.remove(path[row-1])
    if cmd == 'u':
        if row > 1:
            e = path[row-1]
            path[row-1] = path[row-2]
            path[row-2] = e
    if cmd == 'm':
        if row < len(path):
            e = path[row]
            path[row] = path[row-1]
            path[row-1] = e
    if cmd  == 's':
        print("saving")
        setPath(path)
# MAIN

path = getPath()

cmd = ' '
while cmd != 'x':
    row = 0
    printPath(path)
    text = input("[a]ppend, [d]elete, move [u]p, [m]ove down, e[x]it, [s]ave: ")
    tin = text.split(' ')
    cmd = tin[0]
    if cmd not in ('adumxs'):
        print("invalid command:", cmd)
        continue
    #print(len(tin))
    if len(tin) > 1:
        rtext = tin[1]
        #print("rtext:", rtext)
        try:
            row = int(rtext)
            #print(row)
            if row < 1 or row > len(path):
                raise Exception()
        except:
            print("invalid row:", rtext)
            continue
    #print("[", cmd, "]", "[", row, "]")
    command(path, cmd, row)

exit(0)