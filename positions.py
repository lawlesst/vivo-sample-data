"""
Load the positions.csv file.
"""

import csv
import json
import sys

import logging
logging.basicConfig(level=logging.INFO)

from rdflib import Graph
from rdflib_jsonld.parser import to_rdf
from vdm.namespaces import ns_mgr
from utils import hash_uri

#Data namespace
ns = "http://vivo.school.edu/individual/"

pos_ctx = {
    "@context": {
        "@base": ns,
        "a": "@type",
        "uri": "@id",
        "vivo": "http://vivoweb.org/ontology/core#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "label": "rdfs:label",
        "relates": {
            "@id": "vivo:relates",
            "@type": "@id"
        }
    }
}

positions = []

with open(sys.argv[1]) as infile:
    for count, row in enumerate(csv.DictReader(infile)):
        fac_id = row['person_ID']
        org_id = row['department_ID']
        title = row['job_title']

        #Create a hash local name for use in the URI.
        uri_parts = "{}{}{}".format(fac_id, org_id, title)
        position_uri = hash_uri(uri_parts, prefix='pos')

        pos = {}
        pos['uri'] = position_uri
        pos['a'] = 'vivo:FacultyPosition'
        pos['label'] = title
        #Multiple relation statements as list.
        pos['relates'] = [
            'fac{}'.format(fac_id),
            'org{}'.format(org_id)
        ]

        pos.update(pos_ctx)
        positions.append(pos)



raw_jld = json.dumps(positions)
g = Graph().parse(data=raw_jld, format='json-ld')
g.namespace_manager = ns_mgr
print g.serialize(format='turtle')



