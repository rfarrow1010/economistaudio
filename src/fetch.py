#!/usr/bin/env python

# Author: Ryan Farrow
# Date created: 10 Apr 2020

# For reference: https://people.csail.mit.edu/hubert/pyaudio/#docs
# pydub: https://github.com/jiaaro/pydub
# simpleaudio: https://simpleaudio.readthedocs.io/en/latest/tutorial.html

import wave
import time
import sys, os

def get_files(path):
    '''
    Returns a list of files to be played in sequence in a given 
    directory.
    PARAM:
    path: path to directory
    '''

    flist = []

    for files in os.walk(path):
        for item in files[2]:
            if item in flist:
                continue
            elif item.endswith('.mp3'):
                flist.append(item)

    return sorted(flist)

# for controls e.g. restart, go 10 seconds back, change audio
# may need some sneaky start and stop with pydub
# kill a subprocess playing the audio file, create new file object
# with altered parameters, then export it and play whatever that is