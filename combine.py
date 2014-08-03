"""
Combine the RDF files into a graph.
"""

import glob

from rdflib import Graph
from rdflib.util import guess_format

from utils import ns_mgr

g = Graph()
g.namespace_manager = ns_mgr

for item in glob.glob('data/rdf/*'):
    if item == 'all.ttl':
        continue
    format = guess_format(item)
    g.parse(item, format='turtle')


print g.serialize(format='turtle')



