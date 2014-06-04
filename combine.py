"""
Load the organizations.csv file.
"""

import glob
import sys

import logging
logging.basicConfig(level=logging.INFO)

from rdflib import Graph
from rdflib.util import guess_format

from utils import ns_mgr

g = Graph()
g.namespace_manager = ns_mgr

for item in glob.glob('rdf/*'):
    format = guess_format(item)
    g.parse(item, format='turtle')


print g.serialize(format='turtle')



