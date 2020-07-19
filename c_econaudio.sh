#!/bin/bash
# Program to be called
PROG="playecon.py "
# build the Python extension for ncurses
cd src
# CC=gcc python setup.py build
CC=gcc python setup.py install
cd ..

# handle command line args
if [ "$1" != "" ]; then
    PROG += "$1"
fi
if [ "$2" != "" ]; then 
    PROG += "$2"
fi 

python $PROG