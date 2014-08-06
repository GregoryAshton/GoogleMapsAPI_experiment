import simplejson, urllib
import random

DISTANCEMATRIX_BASE_URL = 'http://maps.googleapis.com/maps/api/distancematrix/json'

def get_data(origin, destination, **geo_args):
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
    duration_s, distance_m, v_ave_kmph = get_data(origin, destination)
    print "{} to {} is {} km, takes {} hours so v_ave = {} km/h".format(
           origin, destination, distance_m*1e-3, duration_s/(60.0*60), v_ave_kmph)

if __name__ == '__main__':
    test()
