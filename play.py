#!/usr/bin/env python

# Creates subprocess that plays audio, allowing parent process to take inputs 
# Requires mp3info to be present on the machine

# Author: Ryan Farrow
# Date created: 11 Apr 2020

import os, signal, subprocess
import time

# main file needs to intelligently use the return value here to restart the 
def playfile(dpath, audioname):
    '''
    Plays the file at the target directory with the target name.

    dpath: The path to the directory containing the target file
    audioname: The name of the file to be played

    Returns result of user input. -1 if restarting this track, -2 if going back to 
    previous track, 1 if jumping to next track, 2 if user terminates playback (results in 
    program closing), and 0 if playback finishes normally.
    '''
    r = 0

    # spawns child process that plays audio
    fpath = os.path.join(dpath, audioname)
    sub = subprocess.Popen(['afplay', '{}'.format(fpath)])

    # parent process info
    print(f"Now playing: {audioname}")
    print("Enter \'q\' to quit, \'a\' to rewind/go back one track,")
    print("or \'d\' to jump to next track")
    print(" ")

    # finds runtime of audio file with a system call to mp3info
    call_path = dpath + '/\"' + audioname + '\"'
    runtime = subprocess.check_output('mp3info -p \"%S\\n\" ' + call_path, shell=True)
    int_runtime = int(runtime)

    start = time.time()

    #print('runtime val: ' + str(runtime))

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
                status = os.wait()
                r = status[1] >> 8

            # if so, exit loop
            except ChildProcessError:
                break

        try:
            os.kill(fpid, signal.SIGKILL)
        except OSError:
            print("Input checker closed by itself")

        try:
            os.kill(sub.pid, signal.SIGKILL)
        except OSError:
            print("Audio player closed by itself")

        print(audioname + ' finished')
        print(f"r = {r}")
        return r

    # child process
    else:
        while True:
            uin = input()

            if uin == 'q':
                # user ends playback
                # using child's PID, sends kill signal
                os.kill(sub.pid, signal.SIGKILL)
                print(audioname + " terminated by user")
                r = 2
                exit(r)

            elif uin == 'a':
                os.kill(sub.pid, signal.SIGKILL)
                # within 5 seconds of start of track
                # in this case, go back to track before
                if time.time() - start > 5:
                    r = -2
                    print("Going back one track")
                # not within 5 seconds of start so just rewind this track
                else:
                    r = -1
                    print(f"Restarting {audioname}")

                exit(r)

            elif uin == 'd':
                os.kill(sub.pid, signal.SIGKILL)
                # no matter what the track time is, this will skip to next
                r = 1
                print("Skipping to next track")
                exit(r)

            else:
                print("Invalid input")

        exit(r)