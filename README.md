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
Curently this requires data to be downloaded from [Dan Gibbs git repo](https://github.com/Gibbs/UK-Postcodes)

Dependencies
------------
+ simplejson

   ``$ pip install simplejson``
