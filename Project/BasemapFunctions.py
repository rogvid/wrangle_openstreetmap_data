from geopy.geocoders import Nominatim
from mpl_toolkits.basemap import Basemap
import pickle
import os


def load_cache():
    home = os.path.expanduser("~")
    cache_path = os.path.join(home, "countries.pkl")
    # print "Checking for country cache..."
    if os.path.exists(cache_path):
        # print "Country cache found. Loading..."
        cache = pickle.load(open(cache_path, "rb"))
        # print "Country cache loaded..."
    else:
        # print "Country cache not found. Instantiating empty country cache..."
        cache = {}
        # print "Country cache instantiated..."
    return cache


def get_country_latlon(country):
    cache = load_cache()
    geolocator = Nominatim()
    location = geolocator.geocode(country)
    raw = location.raw
    latlon = map(float, raw['boundingbox'])
    llclat = latlon[0]
    urclat = latlon[1]
    llclon = latlon[2]
    urclon = latlon[3]
    cache[country] = {'llclat': llclat, 'llclon': llclon,
                      'urclat': urclat, 'urclon': urclon}
    home = os.path.expanduser("~")
    cache_path = os.path.join(home, "countries.pkl")
    pickle.dump(cache, open(cache_path, "wb"))
    return llclat, urclat, llclon, urclon


def saveCountry(country):
    cache = load_cache()
    home = os.path.expanduser("~")
    cache_path = os.path.join(home, "countries.pkl")
    geolocator = Nominatim()
    location = geolocator.geocode(country)
    raw = location.raw
    latlon = map(float, raw['boundingbox'])
    llclat = latlon[0]
    urclat = latlon[1]
    llclon = latlon[2]
    urclon = latlon[3]
    cache[country] = {'llclat': llclat, 'llclon': llclon,
                      'urclat': urclat, 'urclon': urclon}
    pickle.dump(cache, open(cache_path, "wb"))


def draw_latlon(llclat, urclat, llclon, urclon,
                rsphere=6371200, resolution='h',
                area_thresh=0.1):
    m = Basemap(llcrnrlat=llclat, urcrnrlat=urclat,
                llcrnrlon=llclon, urcrnrlon=urclon,
                rsphere=rsphere, resolution=resolution,
                area_thresh=area_thresh)
    m.drawcoastlines()
    m.drawcountries()


def draw_country(country, rsphere=6371200, resolution='h', area_thresh=0.1):
    cache = load_cache()
    if not bool(cache):
        llclat, urclat, llclon, urclon = get_country_latlon(country)
    elif country.lower() not in [k.lower() for k in cache.keys()]:
        llclat, urclat, llclon, urclon = get_country_latlon(country)
    else:
        llclat = cache[country]['llclat']
        urclat = cache[country]['urclat']
        llclon = cache[country]['llclon']
        urclon = cache[country]['urclon']
    m = Basemap(llcrnrlat=llclat, urcrnrlat=urclat,
                llcrnrlon=llclon, urcrnrlon=urclon,
                rsphere=rsphere, resolution=resolution,
                area_thresh=area_thresh)
    m.drawcoastlines()
    m.drawcountries()


def coordinates_to_country(latitude, longitude):
    cache = load_cache()
    for country in cache.keys():
        if ((cache[country]['llclat'] <= float(latitude)) and
           (cache[country]['urclat'] >= float(latitude)) and
           (cache[country]['llclon'] <= float(longitude)) and
           (cache[country]['urclon'] >= float(longitude))):
            result = country
            # print "Country found in cache!"
            return result
    geolocator = Nominatim()
    location = geolocator.reverse("{0}, {1}".format(latitude, longitude), language='en')
    country = location.raw['address']['country']
    saveCountry(country)
    return location.raw['address']['country']


def country_basemap(country, rsphere=6371200, resolution='h', area_thresh=0.1):
    cache = load_cache()
    if not bool(cache):
        llclat, urclat, llclon, urclon = get_country_latlon(country, cache)
    elif country.lower() not in [k.lower() for k in cache.keys()]:
        llclat, urclat, llclon, urclon = get_country_latlon(country, cache)
    else:
        llclat = cache[country]['llclat']
        urclat = cache[country]['urclat']
        llclon = cache[country]['llclon']
        urclon = cache[country]['urclon']
    m = Basemap(llcrnrlat=llclat, urcrnrlat=urclat,
                llcrnrlon=llclon, urcrnrlon=urclon,
                rsphere=rsphere, resolution=resolution,
                area_thresh=area_thresh)
    return m


def country_latlon(country):
    cache = load_cache()
    if not bool(cache):
        llclat, urclat, llclon, urclon = get_country_latlon(country, cache)
    if country.lower() not in [k.lower() for k in cache.keys()]:
        llclat, urclat, llclon, urclon = get_country_latlon(country, cache)
    else:
        llclat = cache[country]['llclat']
        urclat = cache[country]['urclat']
        llclon = cache[country]['llclon']
        urclon = cache[country]['urclon']
    return llclat, urclat, llclon, urclon
