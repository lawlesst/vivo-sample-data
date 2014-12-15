"""
Common functions.
"""

import csv
import sys
import time

from fuzzywuzzy import utils as fuzzutils

import requests
requests.packages.urllib3.disable_warnings()
#Cache if we can
try:
    import requests_cache
    requests_cache.install_cache('./data/vivocrawling')
    caching = True
except ImportError:
    caching = False
    pass

DELAY_LENGTH = 1

from rdflib import Graph

def cached_graph(url, delay=False):
    """
    Return a RDFLib graph from an HTTP url.
    Will use caching above if available.
    """
    g = Graph()
    try:
        rsp = requests.get(
            url,
            headers={'Accept': 'application/rdf+xml', 'User-Agent': 'http://vivo.brown.edu'},
            verify=False)
    except RuntimeError:
        print>>sys.stderr, "Failed to parse", url
        return g
    if (delay is True) and ((rsp.from_cache is False) or (caching is False)):
        print>>sys.stderr, "-- crawl delay --"
        time.sleep(DELAY_LENGTH)
    try:
        g.parse(data=rsp.content)
    except Exception, e:
        print>>sys.stderr, e
        return
    return g


def text_normalize(raw):
    """
    Borrow normalization from fuzzywuzzy.
    This uses ascii; should be replaced.
    """
    #make ascii
    araw = fuzzutils.asciidammit(raw)
    #use full process to strip whitespace and lowercase
    fuzzed = fuzzutils.full_process(araw)
    #Replace multiple spaces with single.
    return ' '.join(fuzzed.split())


class ORefRow(object):
    """
    Helper for reading values from OrgRef csv.
    """
    def __init__(self, data):
        self.data = data

    def __getattr__(self, key):
        return self.fetch_cell(key)

    def fetch_cell(self, name):
        """
        Return None instead of blank string for
        empty cells
        """
        v = self.data[name].strip()
        if v == "":
            return None
        else:
            return v


def read_oref_csv(fname):
    with open(fname) as infile:
        for row in csv.DictReader(infile):
            yield ORefRow(row)