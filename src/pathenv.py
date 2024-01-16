import os
import ctypes
import winreg

regdir = "Environment"
hkey = winreg.HKEY_CURRENT_USER
adminhkey = winreg.HKEY_LOCAL_MACHINE
adminregdir = "System\\CurrentControlSet\\Control\\Session Manager\\Environment"
keyname = "Path"
keyvalue = ""

is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
if is_admin:
    hkey = adminhkey
    regdir = adminregdir

def setRegistry(regdir, keyname, keyvalue):
    with winreg.CreateKey(hkey, regdir) as _:
        with winreg.OpenKey(hkey, regdir, 0, winreg.KEY_WRITE) as writeRegistryDir:
            winreg.SetValueEx(writeRegistryDir, keyname, 0, winreg.REG_SZ, keyvalue)

def getRegistry(regdir, keyname):
    with winreg.OpenKey(hkey, regdir) as accessRegistryDir:
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
    if is_admin:
        print("\nSystem Path for Administrator\n")
    else:
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