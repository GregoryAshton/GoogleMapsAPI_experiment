Results 
=======

In this file I've collected some of the interesting results from this experiment. 
I'm sure there is more that can be done, but this is at least a start.

Number of data points
---------------------

Firstly lets check that we have generated a sufficient amount of data for the
results to be meaningful. This can be done by simply plotting a bar-chart of
the number of data points per country:

<img src="./img/HistogramDataCount.png" 
     alt="Histogram of the data count for each country" 
>
It appears that apart from a per countries, we have generated over 1000 data
points for most of the countries. In the future analysis we should be wary
of results from those countries with the smallest data count: GF (French Guiana),
MK (Macedonie), and DO (Dominican Republic). 

Averaged velocities
-------------------

The first and easiest question to ask the data is: "which country is the
fastest?". Of course this comes with a huge number of caveats due to the data
collection technique. Nevertheless taking a naive approach and just averaging
the journey velocities grouped by country we can plot the averaged velcity in
increasing order:

<img src="./img/AverageVelocityPerCountry.png" 
     alt="Average Velocity per Country" 
>
This paints a somewhat surprising picture: the fastest country (by this metric)
is the US. This doesn't fit with many peoples expectations and we might guess
this has something to do with the difference in size between the US and other
countries. 

The US should really be thought of as a collection of smaller countries (the 
individual states). If we don't do this, then picking any two points randomly
by zip code in the US you will be more likely to pick a long-distance journey
than picking any two points in another smaller country. The result is that 
almost all the journeys in the US are along interstate highways. I suspect 
that this causes a bias for faster journeys. 

Velocity Profile
----------------

A more interesting way to investigate the data is to look at the "velocity 
profile" in a country. This described the distribution of journey speeds in 
that country and is calculated by binning all the individual journeys in a 
histogram. 

For example lets compare a fast country Germany (DE) with a slower country such
as Turkey (TR)

<img src="./img/DE_TR.png" 
     alt="Comparing velocity profile of DE and TR" 
     height="300" width="500"
>

There is a marked difference in the distributions. Namely the slower country
has a much longer tail in the increasing velocity direction while the faster
countries velocity drops off sharply. This suggests the vehicles in the faster
country are limited by a speed limit while in the slower country this is not 
the case.

### Some interesting cases
These two examples are quite interesting due to their double peaks 

#### Bangladesh

<img src="./img/BD.png" 
     alt="Velocity profile of BD" 
     height="300" width="500"
>

#### Italy

<img src="./img/IT.png" 
     alt="Velocity profile of BD" 
     height="300" width="500"
>
#### Ones that people might want to see
<img src="./img/GB.png" 
     alt="Velocity profile of BD" 
     height="300" width="500"
>
<img src="./img/MX.png" 
     alt="Velocity profile of BD" 
     height="300" width="500"
>
<img src="./img/US.png" 
     alt="Velocity profile of BD" 
     height="300" width="500"
>






