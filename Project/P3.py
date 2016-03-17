#!/usr/bin/env python
import pprint
from pymongo import MongoClient


def plotLatLon(data):
    import BasemapFunctions as bf
    import matplotlib
    # Set backend to TkAgg because for some reason every other
    # backend makes the ipython console run very very slow
    matplotlib.use('TkAgg')
    import matplotlib.pylab as plt

    # Get basemap of denmark
    bmap = bf.country_basemap("Denmark")
    bmap.drawmapboundary(fill_color='#000000')
    bmap.fillcontinents(color='#f6f7df',lake_color='#000000')
    bmap.drawcoastlines()
    bmap.drawcountries()

    # Set the x and y limit so that we get a closeup of copenhagen and malmo
    plt.ylim(55.3329, 55.8544)
    plt.xlim(12.35, 13.1)
    x = []
    y = []
    # Add all the positions to an array to be plotted on the map
    for r in data:
        x.append(r["pos"][1])
        y.append(r["pos"][0])
    plt.plot(x, y, 'o', c='#862626', alpha=0.5, markersize=0.5, markeredgecolor='none')
    plt.show()


def get_db(db_name):
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def get_addresses():
    # complete the aggregation pipeline
    match = {'$match': {'address.street': {'$exists': 1}}}
    limit = {'$limit': 10}
    pipeline = [match, limit]
    return pipeline

def aggregate(db, pipeline):
    return [doc for doc in db.cities.aggregate(pipeline)]

def get_malmo_positions():
    lon = 12.84
    lat = 55.3458
    match = {'$match': {'$and': [{'pos.0': {'$gte': lat}}, {'pos.1': {'$gte': lon}}]}}
    pipeline = [match]
    return pipeline

def get_amenities():
    match = {'$match': {'amenity': {'$exists': 1}}}
    group = {'$group': {'_id': '$amenity', 'count': {'$sum': 1}}}
    sort = {'$sort': {'count': -1}}
    pipeline = [match, group, sort]
    return pipeline

def show_osak():
    match = {'$match': {'osak:street': {'$exists': 1}}}
    limit = {'$limit': 10}
    pipeline = [match, limit]
    return pipeline

if __name__ == '__main__':
    """
    The following lines were used to audit the mongodb database
    I was unaware that the python code should be handed in, but I've tried
    to add some of the aggregation pipelines I used
    """
    db = get_db('openstreetmap')

    # Prints out 10 addresses. This was how I found the OSAK keys
    result = aggregate(db, get_addresses())
    pprint.pprint(result)

    # Was used to show some of the documents with OSAK keys
    result = aggregate(db, show_osak())
    pprint.pprint(result)

    # Prints out the top amenties. Because I was interested in finding the
    # bicycle pumps and the like, I was interested in the single bicycle pump
    # in the dataset. When I looked it up it turned out to be in sweden, so
    # code indirectly led me to find out that much of the data was in sweden.
    result = aggregate(db, get_amenities())
    pprint.pprint(result)

    # Gets all the documents where position is in Sweden
    result = aggregate(db, get_malmo_positions())
    pprint.pprint(result)

    # Plots the results to confirm suspicion
    plotLatLon(result)
