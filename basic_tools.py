#!/usr/bin/python

import simplejson, urllib
import random
import os
import pandas as pd
import argparse
import matplotlib.pyplot as plt

DISTANCEMATRIX_BASE_URL = 'http://maps.googleapis.com/maps/api/distancematrix/json'

def GetData(origin, destination, **geo_args):
    geo_args.update({
        'origins' : origin,
        'destinations' : destination, 
        'mode' : 'driving',
    })

    url = DISTANCEMATRIX_BASE_URL + '?' + urllib.urlencode(geo_args)
    result = simplejson.load(urllib.urlopen(url))
    data = result['rows'][0]['elements'][0]
    duration = float(data['duration']['value'])
    distance = float(data['distance']['value'])
    v_ave = m_per_s_TO_kmph(distance/duration)
    return duration, distance, v_ave

def m_per_s_TO_kmph(vel_mps):
    return vel_mps * 1e-3 * (60.0 * 60.0)

def random_line():
    " Pick random line from file http://stackoverflow.com/questions/3540288/how-do-i-read-a-random-line-from-one-file-in-python"
    source_file = open("./UK-Postcodes/postcodes.csv")
    line = next(source_file)
    for num, aline in enumerate(source_file):
      if random.randrange(num + 2): continue
      line = aline
    return line.split(",")

def get_origin_destination():
    lineA = random_line()
    postcodeA = lineA[0][1:-1]
    lineB = random_line()
    postcodeB = lineB[0][1:-1]

    return postcodeA, postcodeB

def test():
    origin, destination = get_origin_destination()
    duration_s, distance_m, v_ave_kmph = GetData(origin, destination)
    print "{} to {} is {} km, takes {} hours so v_ave = {} km/h".format(
           origin, destination, distance_m*1e-3, duration_s/(60.0*60), v_ave_kmph)

def UpdateResults(file_name, results):
    """ Look for existing file and append new results, if it doesn't 
        exist then create it

    parameters
    ----------
    file_name : str
        file path to save
    results : dict
        Dictionary of columns and values to save
    """
    if os.path.isfile(file_name):
        df = pd.read_csv(file_name, sep=" ", skipinitialspace=True)
        df = df.append(results, ignore_index=True)
    else:
        df = pd.DataFrame(results, index=[0])
    df.to_csv(file_name, sep=" ")   

def CollectResults(N):
    for i in range(N):
        file_name = "Results_UK.txt"
        origin, destination = get_origin_destination()
        try:
            duration_s, distance_m, v_ave_kmph = GetData(origin, destination)
            results = {'origin' : origin,
                       'destination' : destination,
                       'duration_s' : duration_s,
                       'distance_m' : distance_m,
                       'v_ave_kmph' : v_ave_kmph
                      }
            UpdateResults(file_name, results)
        except KeyError:
            pass

def PlotResults():
    file_name = "Results_UK.txt"
    df = pd.read_csv(file_name, sep=" ", skipinitialspace=True)
    plt.plot(df.duration_s, df.distance_m, "o")
    plt.show()
    
def _setupArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--CollectResults",
                        action="store_true", help=CollectResults.__doc__)
    parser.add_argument("-N", default=100, type=int,
                        help="Number of points to add to file_name")
    parser.add_argument("-p", "--PlotResults", 
                        action="store_true", help=PlotResults.__doc__)
    return parser.parse_args()

if __name__ == "__main__":
    args = _setupArgs()
    if args.CollectResults:
        CollectResults(args.N)
    if args.PlotResults:
        PlotResults()
