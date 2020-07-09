#!/usr/bin/env python

# Author: Ryan Farrow
# Date created: 23 Jun 2020

def catalogue(playlist):
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
                cat["Obituary"] = playlist.index(a)
                    
            else:
                # chop off .mp3 from section headers
                cat[sections[0][:-4]] = playlist.index(a)
                # remove this header
                sections.pop(0)


    return cat

def print_cat(cat):
    '''
    Prints the catalogue in readable format. Returns void.
    '''
    RSPACE = 4

    lspace = max(map(len, cat.keys())) + 1

    newheads = cat.keys()
    # format the strings
    for h in newheads:
        h.ljust(lspace)

    newvals = list(map(str, cat.values()))
    for v in newvals:
        v.rjust(RSPACE)

    # plus 1 for center divider in table
    print('-'*(lspace+RSPACE+1))
    for i, h in enumerate(newheads):
        print(f"{h}|{newvals[i]}")

    print('-'*(lspace+RSPACE+1))

    return
    