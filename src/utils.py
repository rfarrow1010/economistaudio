#!/usr/bin/env python

# Author: Ryan Farrow
# Date created: 23 Jun 2020

# note: may just need to use the Python curses library documented here:
# https://docs.python.org/3/howto/curses.html

import curses

def catalogue(playlist, labels):
    '''
    Catalogues the articles into sections based on topic.

    Return a dict with strings of section names as keys and their indices
    in the playlist as values.
    '''

    i = 0

    sections = [
        "Leaders.mp3",
        "United States.mp3",
        "The Americas.mp3",
        "Briefing.mp3",
        "Asia.mp3",
        "Middle East and Africa.mp3",
        "Europe.mp3",
        "Britain.mp3",
        "International.mp3",
        "Special report.mp3",
        "Business.mp3",
        "Finance and economics.mp3",
        "Science and technology.mp3",
        "Books and arts.mp3",
        "Graphic detail.mp3",
        "Obituary -"
    ]

    cat = {}
    cat["Introduction"] = 0

    for a in playlist:
        if sections[0] in a:
            if sections[0] is "Obituary -":
                cat["Obituary"] = labels[playlist.index(a)]
                    
            else:
                # chop off .mp3 from section headers
                cat[sections[0][:-4]] = labels[i]
                # remove this header
                sections.pop(0)
            i += 1

    return cat

def cat_to_str(cat):
    '''
    Transforms the catalogue to be a formatted string. Returns the string.
    '''
    RSPACE = 4
    lspace = max(map(len, cat.keys())) + 1

    s = f""

    newheads = cat.keys()
    # format the strings
    for h in newheads:
        h.ljust(lspace)

    newvals = list(map(str, cat.values()))
    for v in newvals:
        v.rjust(RSPACE)

    # plus 1 for center divider in table
    s += ('-'*(lspace+RSPACE+1))
    s += '\n'
    for i, h in enumerate(newheads):
        s += f"{h}|{newvals[i]}"

    s += ('-'*(lspace+RSPACE+1))

    return s
    
def last_call(uin, playlist, index):
    '''
    Produces a string describing the previous user call, which 
    will be displayed as the first line of the ncurses terminal 
    output. Takes in the previous user input and the most recently 
    played track. Returns the string. No newline at the end.
    '''
    # jump back a track
    if uin == 'p':
        return f"Jumped back from {playlist[index + 1]}"
    # rewind this track
    elif uin == 'z':
        return f"Rewound {playlist[index]}"
    # jump to next track
    elif uin == 'n':
        return f"Jumped forward from {playlist[index - 1]}"
    # nothing
    else:
        return ""

def curses_ui(audioname, catstring, lastcall):
    '''
    Python-based curses UI function. Invokes the curses terminal API, displays
    info, and then returns the user-input value.

    Accepts the name of the track currently being played, the string representing 
    the catalogue, and the details of the previous user input, if applicable.
    '''
    uin = 0
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    stdscr.addstr(lastcall)
    stdscr.addstr("\n\n")

    stdscr.addstr(f"Now playing: {audioname}\n")
    stdscr.addstr("Press q to quit, right key -> to rewind/go back one track,\n")
    stdscr.addstr("or left key <- to jump to the next track.\n")
    stdscr.addstr("Want to jump to a section? Press that section's corresponding key in the table below.\n\n")

    stdscr.addstr(catstring)
    stdscr.refresh()

    while True:
        uin = stdscr.getch()

        # right key
        if uin == curses.KEY_RIGHT:
            uin = ord('n')
            break
        elif uin == curses.KEY_LEFT:
            uin = ord('p')
            break 
        elif uin == ord('q'):
            break

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

    return uin

def debug(msg):
    '''
    Writes debug info to a file in relative location data/debug.txt.
    Returns null.
    '''
    f = open("data/debug.txt", "a")
    f.write(msg)
    f.write('\n')
    f.close()
