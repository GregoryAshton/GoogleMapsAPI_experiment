#!/usr/bin/python
"""
README

This script takes two arguments at the moment. Call it as either:

    $ python pub_walk.py data

This will generate a comma-deliminated file "pubs_data.txt" with all the 
distances and durations. Or

    $ python pub_walk.py read

This will read the data file and print a list of tuples with the data inside

"""

import simplejson, urllib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc_file
import sys
rc_file("./mpl_rc")

DISTANCEMATRIX_BASE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'

def GetDataWalking(origin, destination, **args):
    """ Function to talk to Google API """
    args.update({
        'origins' : origin,
        'destinations' : destination, 
        'mode' : 'walking',
        'units' : 'metric'
        })
    url = DISTANCEMATRIX_BASE_URL + '?' + urllib.urlencode(args)
    result = simplejson.load(urllib.urlopen(url))
    try:
        data = result['rows'][0]['elements'][0]
    except IndexError:
        print("Downloaded data: ", result)
        raise LookupError("The downloaded data does not match expectations")

    duration = float(data['duration']['value'])
    distance = float(data['distance']['value'])
    return duration, distance

INFO = {"The Craft Beer Co. - Clerkenwell":"82 Leather Ln London EC1N 7TR",
        "Brewdog - Camden":"113 Bayham Street Camden",
        "Euston Tap":"190 Euston Rd, London, United Kingdom",
        "Waterloo Station":"Waterloo Station, Waterloo Rd, London, United Kingdom",
        "Victoria Station":"Victoria St London SW1E 5ND",
        "Dirty Dicks":"202 Bishopsgate, London, United Kingdom",
        "Albert":"Victoria St London SW1H 0NP"}

PUBS = INFO.keys()

if "data" in sys.argv:
    write_file = open("pubs_data.txt", "w+")
    write_file.write("# PubA PubB duration [s] distance [m]\n") 
    N = len(PUBS)
    for i in range(N):
        pubA = PUBS[i]
        for j in range(i+1, N):
            pubB = PUBS[j]
            duration, distance = GetDataWalking(INFO[pubA], INFO[pubB])
            write_file.write("{}, {}, {}, {} \n".format(pubA, pubB, 
                                                  duration, distance))
    write_file.close()

if "read" in sys.argv:
    data = np.genfromtxt("./pubs_data.txt", delimiter=",", dtype=None)
    print data

