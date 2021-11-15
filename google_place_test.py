import googlemaps
from datetime import datetime

def getLoc(addr):
    f = open('api_key.txt','r')
    line = f.readline()
    API_KEY = line
    gmaps = googlemaps.Client(key=API_KEY)
    geocode_result = gmaps.geocode(addr)
    n_lat = geocode_result[0]['geometry']['location']['lat']
    n_lng = geocode_result[0]['geometry']['location']['lng']
    loc = {'lat':n_lat, 'lng':n_lng}
    return loc
getLoc('순천시 왕지동')
