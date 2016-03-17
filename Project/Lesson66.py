#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict
"""
The following script was used to parse the osm data and get it into the mongoDB database

"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def parse_tag(key, value, entry):
    """ Parses a tag for important information """
    key = key.strip()
    if lower.search(key):
        entry[key] = value
    elif key.startswith("addr:") and not key.count(":") > 1:
        address_key = key.split(":")[1]
        if 'address' in entry.keys():
            entry['address'][address_key] = value
        else:
            entry['address'] = {address_key: value}
    elif lower_colon.search(key):
        entry[key] = value

    return entry


def shape_element(element):
    """ Shapes the documents from nodes and ways """
    node = {}
    if element.tag == "node" or element.tag == "way" :
        node['type'] = element.tag
        created = {}
        pos = [None, None]
        for attribute in element.attrib.keys():
            if attribute == 'lat':
                pos[0] = float(element.attrib[attribute])
            elif attribute == 'lon':
                pos[1] = float(element.attrib[attribute])
            elif attribute in CREATED:
                created[attribute] = element.attrib[attribute]
            else:
                node[attribute] = element.attrib[attribute]
        if len(created) > 0:
            node['created'] = created
        if pos != [None, None]:
            node['pos'] = pos
        node_refs = []
        for tag in element:
            if tag.tag == 'tag':
                # print tag.get('k'), tag.get('v')
                node = parse_tag(tag.get('k'), tag.get('v'), node)
            elif tag.tag == 'nd':
                node_refs.append(tag.get('ref'))
        if len(node_refs) > 0:
            node["node_refs"] = node_refs
        #print node
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # Iterates through the OSM file and saves the documents to a json
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data



if __name__ == "__main__":
    osm_filepath = 'C:/Users/rogvid/Dropbox/OOC/Nanodegree/Data Analyst/P3 - Wrangle OpenStreetMap Data/data/copenhagen_denmark.osm'
    data = process_map(osm_filepath, True)
