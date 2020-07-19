#!/usr/bin/env python

# Author: Ryan Farrow
# Date created: 10 Apr 2020

# https://docs.python-guide.org/writing/structure/

# For the terminal scripting:
# https://unix.stackexchange.com/questions/43075/how-to-change-the-contents-of-a-line-on-the-terminal-as-opposed-to-writing-a-new
# http://www.tldp.org/HOWTO/NCURSES-Programming-HOWTO/intro.html

import wave
import time
import sys, os, subprocess, shutil

from src import fetch, play, unzip, utils

# labels for catalogue navigation
LABELS = [
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'a',
    's',
    'd',
    'f',
    'g',
    'h',
    'j'
]

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
    audio_player = ''
    playlist = []
    val = 0
    # command line inputs
    if len(sys.argv) >= 2:
        if sys.argv[1] == '-h':
            usage(0)

        elif sys.argv[1] == '-c':
            shutil.rmtree('econdata')

    # interactive prompt
    else:
        if sys.platform == 'darwin':
            audio_player = 'afplay'

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
        catalogue = utils.catalogue(playlist, LABELS)

        while index < 0 or index > len(playlist) - 1:
            index = int(input("Enter number of track you wish to play: ")) - 1

        # play each track starting at index while checking for user input
        while index < len(playlist):
            val = play.playfile(audio_player, zippath, playlist[index], catalogue, utils.last_call(val, playlist, index))

            # index check
            if index < 0:
                index = 0

            # user termination
            if val == ord('q'):
                break

            # skip to next track, increment index
            elif val == ord('n'):
                index += 1 

            # restart this track; index doesn't change
            elif val == ord('z'):
                continue

            # go back to previous track; decrement index
            elif val == ord('p'):
                index -= 1

            # all other cases: assume it timed out, increment index
            else:
                index += 1

            if index >= len(playlist):
                utils.debug("Playlist fully traversed")
                break

if __name__ == "__main__":
    main()