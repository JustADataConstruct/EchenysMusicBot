import json
import sys
from os import listdir
from os.path import abspath, isfile, join

# A helper script to quickly generate playlists. Note that it's a very basic script: it doesn't preserve any kind of
# file order, nor can start or end times be indicated unless the output file is manually edited. It's useful mostly
# for general playlists where you don't need any specific details.


def print_usage():
    print("Usage: playlist.helper.py [MUSIC FOLDER PATH] [PLAYLIST NAME]")
    print("Note: this script will grab every file on the indicated folder.")
    print("Make sure the folder only contains the audio files you want to add to the playlist.")

if len(sys.argv) < 3 :
    print_usage()
    sys.exit()

folder = sys.argv[1]
name = sys.argv[2]
playlist = []

try:
    files = [f for f in listdir(folder) if isfile(join(folder,f))]
    for m in files:
        playlist.append(abspath(join(folder,m)))
except Exception as e:
    print("Something went wrong trying to read from the indicated folder.")
    print(e)
    sys.exit()

olist = []
for m in playlist:
    o = {
        "route":m
    }
    olist.append(o)

try:
    with open("export_playlist.json","w") as o:
        o.write(f'"{name}":{json.dumps(olist,indent=4)}')
except Exception as e:
    print("Something went wrong while trying to save your playlist.")
    print(e)
    sys.exit()

print("Playlist exported! Check your active folder for the export_playlist.json file, and paste its contents into the songs.json file")
input("Press any key to close")
