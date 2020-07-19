#!/usr/bin/env python

from distutils.core import setup, Extension

def main():
    ncurses = Extension('termUtils', sources = ['termUtils.c'])

    setup(name = 'termUtils', version = '1.0', 
        description = 'Package for employing the ncurses terminal features in Economist Command Line Player',
        author='Ryan Farrow',
        ext_modules = [ncurses])

# next step: make a little bash script to do the following
# python setup.py build
# python setup.py install
# {everything else for running the script}

if __name__ == "__main__":
    main()