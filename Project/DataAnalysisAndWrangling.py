# import xml.etree.ElementTree as ET
import lxml.etree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict
import re

filepath = "./data/copenhagen_denmark.osm"
UNIQUE_TAGS = ['bounds', 'member', 'nd', 'node', 'osm', 'relation', 'tag', 'way']

COPENHAGEN = {'country': 'denmark',
              'city': 'copenhagen',
              'bounds': {''}}

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def parse_tag(key, value, entry):
    key = key.strip()
    if lower.search(key):
        entry[key] = value
    elif key.startswith("addr:") and not key.count(":") > 1:
        print key, value
        address_key = key.split(":")[1]
        if 'address' in entry.keys():
            entry['address'][address_key] = value
        else:
            entry['address'] = {address_key: value}
    elif lower_colon.search(key):
        entry[key] = value

    return entry

def parse_elem(element):
    """ Function used to parse the various tags """
    if element.tag == 'node' or element.tag == 'way':
        for tag in element:
            if tag.attrib['v'] not in ['motorway_junction', 'traffic_signals', 'yes', 'JOSM']:
                # print ET.tostring(tag)
                node = parse_tag(tag.attrib['k'], tag.attrib['v'], {})


def parse_osm(filepath, pretty=False, limit=None):
    """ Parses an OpenStreetMap File iteratively """
    lines_parsed = 0
    for _, element in ET.iterparse(filepath):
        # print ET.tostring(element)
        parse_elem(element)
        lines_parsed += 1
        if limit != None:
            if lines_parsed >= limit:
                return


def parse_osm_tag(filepath, tag, limit=None):
    """ Parses Specific tags of an OpenStreetMap File iteratively """
    lines_parsed = 0
    for _, element in ET.iterparse(filepath, tag=tag):
        print ET.tostring(element)
        lines_parsed += 1
        if limit != None:
            if lines_parsed >= limit:
                return


if __name__ == "__main__":
    # parse_osm(filepath, limit=20)
    parse_osm(filepath, limit=10000)
