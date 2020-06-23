#!/usr/bin/env python

# Author: Ryan Farrow
# Date: 16 May 2020

import zipfile
import os 

def unzip(path, cleanup=False, dest=os.path.dirname(os.path.realpath(__file__))):
    """
    Unzips the file with path given in first parameter. Deletes the zip file 
    and puts the new folder in the specified destination, default this file's directory. If cleanup is set to 
    True, then the .zip file will be deleted.

    Returns the path of the unzipped folder (or 0 on failure).
    """

    # make directory to store stuff
    # directory name defined by dest param so can be modified

    # if it is the default dest, append "/data" to it
    if dest == os.path.dirname(os.path.realpath(__file__)):
        dest += "/econdata"

    # if not, just proceed with whatever is supplied
    try:
        os.mkdir(dest)
    except OSError as e:
        print("Could not make directory: " + str(e))

    # check that the given file is a zip file
    if ".zip" in path:
        # use absolute path
        abspath = os.path.abspath(path)
        with zipfile.ZipFile(abspath, "r") as zip:
            zip.extractall(path=dest)

        # remove zip file
        if cleanup:
            try:
                os.remove(abspath)
            except OSError as e:
                print("Could not delete origin")

        return abspath


    # not a zip file
    else:
        print("Supplied file not a zip file")
        return 0

def scan(datascan=True):
    '''
    Scans this file's directory, the Downloads directory, and the Desktop directory 
    for a zip file starting with "Issue_", assumed to be an Economist Audio zip file.
    If it finds the file, it then scans the same directories for a directory called econdata 
    if datascan is True. 

    Returns a tuple whose first member is the path to the zip file (or econdata if it exists) and whose second 
    member is True if it needs unzipping, False otherwise.
    '''
    r = ('', False)

    zipfound = False
    datafound = False

    for root, dirs, files in os.walk("."):
        for f in files:
            if "Issue_" in f:
                r = (os.path.join(root, f), r[1])
                zipfound = True

    if not zipfound:
        for root, dirs, files in os.walk(os.path.join(os.environ['HOME']), "/Downloads"):
            for f in files:
                if "Issue_" in f:
                    r = (os.path.join(root, f), r[1])
                    zipfound = True

    if not zipfound:
        for root, dirs, files in os.walk(os.path.join(os.environ['HOME']), "/Desktop"):
            for f in files:
                if "Issue_" in f:
                    r = (os.path.join(root, f), r[1])
                    zipfound = True

    if not zipfound:
        return r


    if datascan:
        for root, dirs, files in os.walk("."):
            for d in dirs:
                if "econdata" in d:
                    datafound = True
                    r = (os.path.join(root, d), r[1])

        if not datafound:
            for root, dirs, files in os.walk(os.path.join(os.environ['HOME']), "/Downloads"):
                for d in dirs:
                    if "econdata" in d:
                        datafound = True
                        r = (os.path.join(root, d), r[1])

        if not datafound:
            for root, dirs, files in os.walk(os.path.join(os.environ['HOME']), "/Desktop"):
                for d in dirs:
                    if "econdata" in d:
                        datafound = True
                        r = (os.path.join(root, d), r[1])

    if datascan:
        if not datafound:
            r = (r[0], True)

    return r

if __name__ == "__main__":
    unzip("../Desktop/Issue_9194_20200516_The_Economist_Full_edition.zip")
    scan()