""" 
Steam Community > Snowrunner > General Discussion > How to transfer save files from EGS to Steam

Murwen has SnowRunner 18 May, 2021 @ 8:17pm  

The problem with maps not being explored or whatever after you've transfered and renamed 
your old *.dat files is because the renamed files are not indexed in remotecache.vdh. To solve 
this you need to generate an entry for every *.cfg. You can either explore the game manually, 
which sounds pretty tedious, or you can use a python script.

I found an existing script which does this for another game and modified it so that it works for 
Snowrunner saves, I've made it available here: https://pastebin.com/ZhCESujt

(Modified from remotecache.py from https://github.com/zarroboogs/p4g-saveconv )

Anywho, after you've deleted your old remotecache.vdh in step 5 in the OP you should run 
this script in your "1465360" folder, this will generate a shiny new remotecache.vdh. Now 
when you boot up your game all your old progress will be there.
Last edited by Murwen; 31 May, 2022 @ 8:28pm 
"""

import os
import math
import hashlib
import argparse
from pathlib import Path


def sha1sum( stream, start=0 ):
    sha1 = hashlib.sha1()
    stream.seek( start, 0 )

    while True:
        data = stream.read( 1024 )
        if not data:
            break
        sha1.update( data )

    stream.seek( 0, 0 )
    return sha1


def vdf_write( vdf, level, key="", val=None ):
    pad = '\t' * level
    if key == None or key == "":
        vdf.write( f'{pad}' + "}\n" )
    elif val == None:
        vdf.write( f'{pad}"{key}"\n{pad}' + "{\n" )
    else:
        vdf.write( f'{pad}"{key}"\t\t"{val}"\n' )


def write_remcache_file( vdf, filepath ):
    fstat = os.stat( filepath )
    fsize = fstat.st_size
    ftime = math.floor( fstat.st_mtime )

    with open( filepath, "rb" ) as fs:
        fsha = sha1sum( fs ).hexdigest()

    vdf_write( vdf, 1, filepath.name )
    vdf_write( vdf, 2, "root", 0 )
    vdf_write( vdf, 2, "size", fsize )
    vdf_write( vdf, 2, "localtime", ftime )
    vdf_write( vdf, 2, "time", ftime )
    vdf_write( vdf, 2, "remotetime", ftime )
    vdf_write( vdf, 2, "sha", fsha )
    vdf_write( vdf, 2, "syncstate", 4 )
    vdf_write( vdf, 2, "persiststate", 0 )
    vdf_write( vdf, 2, "platformstosync2", -1 )
    vdf_write( vdf, 1 )


def write_remcache( remcache_path, data_path ):
    with open( remcache_path, "w", newline='\n' ) as vdf:
        vdf_write( vdf, 0, "1465360" )

        for f in data_path.glob( "*" ):
            write_remcache_file( vdf, f )

        # for f in data_path.glob( "system.bin" ):
        #     write_remcache_file( vdf, f )
        #     write_remcache_file( vdf, Path( f"{f}slot" ) )

        # for f in data_path.glob( "data*.bin" ):
        #     write_remcache_file( vdf, f )
        #     write_remcache_file( vdf, Path( f"{f}slot" ) )

        vdf_write( vdf, 0 )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument( "save_dir", nargs=1, help="pc save dir" )
    args = parser.parse_args()

    save_path = Path( args.save_dir[ 0 ] )

    if not save_path.is_dir():
        raise Exception( "missing save dir or save dir doesn't exist" )

    # files = [ f for f in save_path.glob( "data*.binslot" ) if f.is_file() ]
    # if len( files ) == 0:
    #     raise Exception( "input dir doesn't contain pc saves" )
    files = [ f for f in save_path.glob( "*.cfg" ) if f.is_file() ]
    if len( files ) == 0:
        raise Exception( "input dir doesn't contain pc saves" )

    print( "generating remotecache.vdf" )
    remcache_path = Path ( save_path.parent / "remotecache.vdf" )
    write_remcache( remcache_path, save_path )

    print( "done!" )


if __name__ == "__main__":
    main()
