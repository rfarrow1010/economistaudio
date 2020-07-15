#!/usr/bin/env python

# Author: Ryan Farrow
# Date created: 23 Jun 2020

def catalogue(playlist, labels):
    '''
    Catalogues the articles into sections based on topic.

    Return a dict with strings of section names as keys and their indices
    in the playlist as values.
    '''

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
                cat[sections[0][:-4]] = labels[playlist.index(a)]
                # remove this header
                sections.pop(0)


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
    
def last_call(uin, track):
    '''
    Produces a string describing the previous user call, which 
    will be displayed as the first line of the ncurses terminal 
    output. Takes in the previous user input and the most recently 
    played track. Returns the string.
    '''

    pass