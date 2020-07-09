#!/usr/bin/env python

# Author: Ryan Farrow
# Date created: 10 Apr 2020

# https://docs.python-guide.org/writing/structure/

import wave
import time
import sys, os, subprocess, shutil

from src import fetch, play, unzip, utils

# note: will need to take options for specifying the path
# no options should first search for a directory, then ask 
# for download link if it is not found

def usage(exitcode=0):
    print('''
    Usage: ./playecon.py [ path/to/mp3folder ]
    Options: -c (clean out econdata)
    Path is optional; if no path is provided,
    interactive prompt will start
    ''')
    exit(exitcode)

def main():
    playlist = []
    # command line inputs
    if len(sys.argv) >= 2:
        if sys.argv[1] == '-h':
            usage(0)

        elif sys.argv[1] == '-c':
            shutil.rmtree('econdata')


    # command line inputs
    elif len(sys.argv) > 1:
        files = fetch.get_files(sys.argv[1])
        #current_fpath = os.path.join(sys.argv[1], files[0])

        if sys.platform == 'darwin':
            play.playfile(sys.argv[1], files[0])

    # interactive prompt
    else:
        if not os.path.isdir("./econdata"):
            (zippath, zipbool) = unzip.scan()
        else:
            (zippath, zipbool) = ("./econdata", False)

        index = -1

        # unzip if it needs unzipping
        if zipbool:
            unzip.unzip(zippath)

        try:
            for items in os.walk("./econdata"):
                for track in items[2]:
                    playlist.append(track) 

            playlist.sort()

        except OSError:
            print("Audio zip file not found. Please download the zip file")
            print("and put it in Downloads, Desktop, or this directory.")
            exit(1)

        if len(playlist) == 0:
            print("Playlist construction failed. Exiting")
            exit(1)
        
        # make catalogue of sections
        cat = utils.catalogue(playlist)

        while index < 0 or index > len(playlist) - 1:
            index = int(input("Enter number of track you wish to play: ")) - 1

        # play each track starting at index while checking for user input
        while index < len(playlist):
            val = play.playfile(zippath, playlist[index])

            # index check
            if index < 0:
                index = 0

            if index >= len(playlist):
                print("Playlist fully traversed")
                exit(0)

            # user termination
            if val == 2:
                exit(0)

            # skip to next track, let the index increment
            elif val == 1:
                continue 

            # all other cases: add val to index for desired result
            else:
                index += val


        if index >= len(playlist):
            print("Playlist fully traversed")
            exit(0)


if __name__ == "__main__":
    main()