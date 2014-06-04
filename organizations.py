"""
Load the organizations.csv file.
"""

import csv
import json
import sys

import logging
logging.basicConfig(level=logging.INFO)

from rdflib import Graph
from utils import ns_mgr

#Data namespace
ns = "http://vivo.school.edu/individual/"

org_ctx = {
    "@context": {
        "@base": ns,
        "a": "@type",
        "uri": "@id",
        "vivo": "http://vivoweb.org/ontology/core#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "label": "rdfs:label",
    }
}

organizations = []

with open(sys.argv[1]) as infile:
    for count, row in enumerate(csv.DictReader(infile)):
        print row
        name = row['org_name']
        oid = row['org_ID']
        org_uri = 'org{}'.format(oid)
        org_type = row['org_vivo_uri']

        org = {}

        org['uri'] = org_uri
        org['a'] = org_type
        org['label'] = name

        org.update(org_ctx)
        organizations.append(org)


raw_jld = json.dumps(organizations)
g = Graph().parse(data=raw_jld, format='json-ld')
g.namespace_manager = ns_mgr
print g.serialize(format='turtle')



