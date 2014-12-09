Google maps travel time experiment
==================================


This project aims to use the travel time data provided by Google through it's
[Distance matrix API](https://developers.google.com/maps/documentation/distancematrix/)
to perform experiments. The results can be found [here](Results.md)

There is a location database and a results database, the locations are latatide
 and longitude pairs taken from [GeoNames](www.geonames.org). The results come
from taking random pairs or lat/long in the same country and calculating the 
distance and time as given by Google's maps API.  

There is a limit of 2500 downloads per day from any given IP or API key, so the
results are saved in this directory so anyone can contribute. To do so simply
clone this repo, follow the installation instructions, then pick a country and
start getting data. This is a Monte Carlo like study so the more data the
better.

Installation:
------------
Install dependencies, if you have pip installed then

``$ sudo pip install simplejson``

``$ sudo pip install pandas``

Now we need to download the location database

``$ cd Location_database``

Then 

``$ make ``

This will download the zip file and extract the data. Once done your all set
simply `cd ../` and do

``$ ./basic_tools --help`` 

to see the options

Basic usage:
------------
+ Get a list of all countries available in the location database, this
  prints a list of the country codes, e.g `GB`=Great Britian 

  ``$ ./basic_tools -g ``

+ Get a list of all the downloaded data so far

  ``$ ./basic_tools -l``

+ Collect data, for example:

  ``$ ./basic_tools -r -N 1000 -c US``

  The `-r` flag initiates the download data script, the `-N` requests 1000
  attempts to collect data, and finally the country is given to `-c` by it's
  country code. 

+ Plot the distance vs time graphs with the flag `-p`, then the countries you
want to include

  ``$ ./basic_tools -p -c GB MX``

+ Velocity distrubution graphs can similarly be obtained from

  ``$ ./basic_tools -v -c US MX``


Dependencies
------------
+ python
+ simplejson
+ pandas
+ numpy
+ matplotlib


