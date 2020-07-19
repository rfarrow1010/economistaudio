#!/usr/bin/env python

# Creates subprocess that plays audio, allowing parent process to take inputs 
# Requires mp3info to be present on the machine

# Author: Ryan Farrow
# Date created: 11 Apr 2020

import os, signal, subprocess, time
import src.utils
import ctypes, pathlib

# main file needs to intelligently use the return value here to restart the 
def playfile(audio_player, dpath, audioname, catalogue, lastcall):
    '''
    Plays the file at the target directory with the target name.

    dpath: The path to the directory containing the target file
    audioname: The name of the file to be played

    Returns result of user input. -1 if restarting this track, -2 if going back to 
    previous track, 1 if jumping to next track, 2 if user terminates playback (results in 
    program closing), and 0 if playback finishes normally.
    '''
    r = 0

    # convert catalogue into string for ncurses to display
    strcat = src.utils.cat_to_str(catalogue)

    # spawns child process that plays audio
    fpath = os.path.join(dpath, audioname)
    sub = subprocess.Popen([audio_player, '{}'.format(fpath)])

    # finds runtime of audio file with a system call to mp3info
    call_path = dpath + '/\"' + audioname + '\"'
    runtime = subprocess.check_output('mp3info -p \"%S\\n\" ' + call_path, shell=True)
    int_runtime = int(runtime)

    start = time.time()

    # note to self: the way to do this might be to fork off a child process that checks for
    # input and have the parent contain the while loop
    # once the while loop concludes, kill child process and print out exit code 0

    fpid = os.fork()

    # parent process
    if fpid > 0:
        # wait for runtime to elapse
        while time.time() < start + int_runtime:
            # check if user has cancelled playback
            try:
                # looking for upper byte of second element in this tuple
                pid, r = os.wait()
                r = r >> 8

            # if so, exit loop
            except ChildProcessError:
                break

        try:
            os.kill(fpid, signal.SIGKILL)
        except OSError:
            pass

        try:
            os.kill(sub.pid, signal.SIGKILL)
        except OSError:
            pass

        return r

    # child process
    else:
        while True:
            # TODO: put the ncurses stuff here
            # read:
            # https://realpython.com/build-python-c-extension-module/
            uin = src.utils.curses_ui(audioname, "", lastcall)

            if uin == ord('q'):
                # user ends playback
                # using child's PID, sends kill signal
                os.kill(sub.pid, signal.SIGKILL)
                exit(uin)

            elif uin == ord('p'):
                os.kill(sub.pid, signal.SIGKILL)
                # not within 5 seconds of start so give signal to rewind this track
                if time.time() - start > 5:
                    uin = ord('z')
                # if it is within 5 seconds, no action needed
                exit(uin)

            elif uin == ord('n'):
                os.kill(sub.pid, signal.SIGKILL)
                # no matter what the track time is, this will skip to next
                exit(uin)

        # if it somehow breaks free of while loop, exit -1
        exit(-1)