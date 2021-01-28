import sys
import json
from os import listdir
from os.path import isfile,join,abspath
from glob import glob

# A helper script to quickly generate playlists. Note that it's a very basic script: it doesn't preserve any kind of
# file order, nor can start or end times be indicated unless the output file is manually edited. It's useful mostly
# for general playlists where you don't need any specific details.


def print_usage():
    print("Usage: playlist.helper.py [MUSIC FOLDER PATH] [PLAYLIST NAME]")
    print("Note: this script will grab every file on the indicated folder.")
    print("Make sure the folder only contains the audio files you want to add to the playlist.")

#TODO: Error handling.
if len(sys.argv) < 3 :
    print_usage()
    sys.exit()

folder = sys.argv[1]
name = sys.argv[2]
playlist = []


files = [f for f in listdir(folder) if isfile(join(folder,f))]
for m in files:
    playlist.append(abspath(join(folder,m)))

olist = []
for m in playlist:
    o = {
        "route":m
    }
    olist.append(o)

print(olist)

with open("export_playlist.json","w") as o:
    o.write(f'"{name}":{json.dumps(olist,indent=4)}')

print("Playlist exported! Check your active folder for the export_playlist.json file, and paste its contents into the songs.json file")
input("Press any key to close")