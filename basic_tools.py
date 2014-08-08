#!/usr/bin/python

import simplejson, urllib
import random
import os
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc_file
import logging
import time
rc_file("./mpl_rc")

DISTANCEMATRIX_BASE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'

def GetCC():
    df = GetLocationData()
    CCs = np.unique(df.CC.values)

    print "List of Country Codes:"
    print "Country codes : # entries"
    for CC in CCs:
        print "{} : {}".format(CC, len(df[df.CC==CC]))

def ListDownloadedData():
    keys = [s.split("_")[1].rstrip(".txt") for s in 
                       os.listdir("./Results_database/")]

    print "CC : Number of data points"
    for key in keys:
        f = GetResultsFile(key)
        df = pd.read_csv(f, sep=" ", skipinitialspace=True)
        print "{} : {}".format(key, len(df.index))

def GetData(origin, destination, **args):
    args.update({
        'origins' : origin,
        'destinations' : destination, 
        'mode' : 'driving',
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
    v_ave = mps_TO_kmph(distance/duration)
    return duration, distance, v_ave

def GetAPIKey(key_file):
    " Reads the API_KEY if it exists, IOError if not"
    with open(key_file, 'r') as f:
      KEY = f.readline().rstrip("\n")
    return KEY

def GetLocationData():
    source_file = "./Location_database/allCountries.txt"
    df = pd.read_table(source_file, sep="\t", encoding="utf8", 
                       usecols=[0, 1, 9, 10], 
                       names=["CC", "ZIP", "lat", "lon"])
    return df

def GetResultsFile(key):
    directory = "./Results_database/"
    file_name = directory+"Results_{}.txt".format(key)
    return file_name

def mps_TO_kmph(vel_mps):
    return vel_mps * 1e-3 * (60.0 * 60.0)


def test():
    df = GetLocationData()
    rns = np.random.uniform(0, df.shape[0], 2)
    origin, destination = df.ix[rns].ZIP.values
    KEY = GetAPIKey()
    duration_s, distance_m, v_ave_kmph = GetData(origin, destination, key=KEY)
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

def CollectResults(N, CC, key_file=None):
    """ Randomly select N pairs of postcodes from Country and save results

    Parameters
    ----------
    N : int
        Integer number of results two collect
    Country : str
        Country code, default is given by the first argument to Country argument
    """

    df = GetLocationData()
    df = df[df.CC == CC]
    df = df.reset_index(drop=True)
    Nrows = df.shape[0]
    if Nrows == 0:
        raise ValueError("{} is not a valud Country Code (CC)".format(CC))
    if Nrows < N:
        logging.warning(("Number of data rows for CC={} is less than requested"
                         "is less thnumber of data points N={}, reducing data" 
                         "rows to N={}").format(CC, N, Nrows))
        N = Nrows

    results_file = GetResultsFile(CC)

    if key_file:
        key = GetAPIKey(key_file)
        kwargs = {'key':key}
    else:
        kwargs = {}

    for i in range(N):
        rns = np.random.randint(0, Nrows, 2)
        lat_orig = df.ix[rns[0]].lat
        lon_orig = df.ix[rns[0]].lon
        origin = str(lat_orig) + "," + str(lon_orig)
        lat_dest = df.ix[rns[1]].lat
        lon_dest = df.ix[rns[1]].lon
        destination = str(lat_dest) + "," + str(lon_dest)
        try:
            duration_s, distance_m, v_ave_kmph = GetData(origin, destination, 
                                                         **kwargs)
            now = time.gmtime()
            now_str = "{}_{}_{}".format(now.tm_year, now.tm_mon, now.tm_mday)
            results = {'origin' : origin,
                       'destination' : destination,
                       'duration_s' : duration_s,
                       'distance_m' : distance_m,
                       'v_ave_kmph' : v_ave_kmph,
                       'time' : now_str
                      }
            UpdateResults(results_file, results)
        except KeyError:
            print "Bad data for {} {}".format(origin ,destination)
        except ZeroDivisionError:
            print "Bad data for {} {}".format(origin ,destination)

def PlotDistanceTime(Countries):
    """Plot the distance against time for Country in Countries """
    for Country in Countries:
        results_file = GetResultsFile(Country)
        df = pd.read_csv(results_file, sep=" ", skipinitialspace=True)

        print "Average speed = {} kmph in {}".format(
                mps_TO_kmph(np.average(df.distance_m)/np.average(df.duration_s)),
                Country)
        plt.plot(df.duration_s, df.distance_m, "o", alpha=0.3,
                 label=Country)

    plt.xlabel("Time [s]")
    plt.ylabel("Distance [m]")
    plt.legend(loc=2, frameon=False)
    plt.show()

def PlotVelocities(Countries, ptype='line', *args, **kwargs):
    """ Plot the velocities of the Countries """
    for Country in Countries:
        results_file = GetResultsFile(Country)
        df = pd.read_csv(results_file, sep=" ", skipinitialspace=True)
        y, binEdges=np.histogram(df.v_ave_kmph, bins=50, normed=True)

        if ptype == 'bar':
            plt.bar(binEdges[:-1], y, width=np.diff(binEdges), 
                    label=Country, **kwargs)
        elif ptype == 'line':
            c = np.random.uniform(0, 1, 3)
            bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            plt.plot(bincenters, y, label=Country, color=c, **kwargs)
            plt.fill_between(bincenters, 0, y, color=c, alpha=0.2)

    plt.xlabel("Velocity [km/h]")
    plt.ylabel("Normalised count")
    plt.legend(loc=2, frameon=False)
    plt.show()

def _setupArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--CollectResults",
                        action="store_true", help=CollectResults.__doc__)
    parser.add_argument("-k", "--KeyFile", default=None, type=str,
                        help="API key file to use in request")
    parser.add_argument("-N", default=100, type=int,
                        help="Number of points to add to file_name")
    parser.add_argument("-p", "--PlotDistanceTime", 
                        action="store_true", help=PlotDistanceTime.__doc__)
    parser.add_argument("-v", "--PlotVelocities", help=PlotVelocities.__doc__,
                        action="store_true")
    parser.add_argument("-c", "--Country", default="UK", type=str, nargs="*",
                        help="Country to use datafile from")
    parser.add_argument("-g", "--GetCountryCodes", action="store_true", 
                        help="Print a list of usable Country codes")
    parser.add_argument("-l", "--ListDownloadedData", action="store_true", 
                        help=ListDownloadedData.__doc__)

    return parser.parse_args()

if __name__ == "__main__":
    args = _setupArgs()
    if args.GetCountryCodes:
        GetCC()
    if args.CollectResults:
        CollectResults(N=args.N, CC=args.Country[0], key_file=args.KeyFile)
    if args.PlotDistanceTime:
        PlotDistanceTime(Countries=args.Country)
    if args.PlotVelocities:
        PlotVelocities(Countries=args.Country)
    if args.ListDownloadedData:
        ListDownloadedData()
