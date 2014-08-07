Google maps travel time experiment
==================================


This project aims to use the travel time data provided by Google through it's
[Distance matrix API](https://developers.google.com/maps/documentation/distancematrix/)
to perform experiments. 

Initially it is limited to measuring the average speed between randomly selected
points in the UK. Extending this to all counrties where data is available means
we can test the question "Which country drives the fastest?".

Notes:
-----
Location data is sourced from [GeoNames](www.geonames.org), so thanks for that.

Dependencies
------------
+ simplejson
   ``$ pip install simplejson``
+ pandas
   ``$ pip install pandas``

And the usual `numpy`, `matplotlib`.
