#!/usr/bin/python

import simplejson, urllib
import random
import os
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc_file
rc_file("/home/greg/Neutron_star_modelling/matplotlibrc")

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
    v_ave = mps_TO_kmph(distance/duration)
    return duration, distance, v_ave

def GetCSVFile(key):
    directory = "./CSV_database/"
    CSV_dict = {"UK" : directory+"postcodes.csv",
                "USA" : directory + "zip_code_database.csv"
               }
    try:
        return CSV_dict[key]
    except KeyError:
        print "CSV key not in exsistence"

def mps_TO_kmph(vel_mps):
    return vel_mps * 1e-3 * (60.0 * 60.0)

def random_line():
    " Pick random line from file http://stackoverflow.com/questions/3540288/how-do-i-read-a-random-line-from-one-file-in-python"
    source_file_name = GetCSVFile(args.Country)
    source_file = open(source_file_name)
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

def CollectResults(N, Country):
    """ Randomly select N pairs of postcodes from Country and save results

    Parameters
    ----------
    N : int
        Integer number of results two collect
    Country : str
        Country code, default is given by the first argument to Country argument
    """

    results_file = "Results_{}.txt".format(Country)
    for i in range(N):
        origin, destination = get_origin_destination()
        try:
            duration_s, distance_m, v_ave_kmph = GetData(origin, destination)
            results = {'origin' : origin,
                       'destination' : destination,
                       'duration_s' : duration_s,
                       'distance_m' : distance_m,
                       'v_ave_kmph' : v_ave_kmph
                      }
            UpdateResults(results_file, results)
        except KeyError:
            pass

def PlotDistanceTime(Countries):
    """Plot the distance against time for Country in Countries """
    for Country in Countries:
        results_file = "Results_{}.txt".format(Country)
        df = pd.read_csv(results_file, sep=" ", skipinitialspace=True)

        print "Average speed = {} kmph".format(
                mps_TO_kmph(np.average(df.distance_m)/np.average(df.duration_s)))
        plt.plot(df.duration_s, df.distance_m, "o", alpha=0.3,
                 label=Country)

        #speed_limit_mph = 70
        #speed_limit_mps = speed_limit_mph * 1609. / (60 * 60)
        #distances = np.linspace(0, 1e7, 100)
        #plt.plot(distances/speed_limit_mps, distances)
    plt.xlabel("Time [s]")
    plt.ylabel("Distance [m]")
    plt.legend(loc=2, frameon=False)
    plt.show()

def PlotVelocities(Countries):
    """ Plot the velocities of the Countries """
    for Country in Countries:
        results_file = "Results_{}.txt".format(Country)
        df = pd.read_csv(results_file, sep=" ", skipinitialspace=True)
        plt.hist(df.v_ave_kmph, bins=50, label=Country, alpha=0.5, normed=True)

    plt.xlabel("Velocity [km/h]")
    plt.ylabel("Normalised count")
    plt.legend(loc=2, frameon=False)
    plt.show()

def _setupArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--CollectResults",
                        action="store_true", help=CollectResults.__doc__)
    parser.add_argument("-N", default=100, type=int,
                        help="Number of points to add to file_name")
    parser.add_argument("-p", "--PlotDistanceTime", 
                        action="store_true", help=PlotDistanceTime.__doc__)
    parser.add_argument("-v", "--PlotVelocities", help=PlotVelocities.__doc__,
                        action="store_true")
    parser.add_argument("-c", "--Country", default="UK", type=str, nargs="*",
                        help="Country to use datafile from")

    return parser.parse_args()

if __name__ == "__main__":
    args = _setupArgs()
    if args.CollectResults:
        CollectResults(N=args.N, Country=args.Country)
    if args.PlotDistanceTime:
        PlotDistanceTime(Countries=args.Country)
    if args.PlotVelocities:
        PlotVelocities(Countries=args.Country)
