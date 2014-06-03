"""
Load the people.csv file as VIVO Faculty Members.

See VCard usage:
https://wiki.duraspace.org/display/VIVO/VCard+usage+diagram

"""

import csv
import json
import sys

from rdflib import Graph

ns = "http://vivo.brown.edu/individual/"

faculty = {
    "@context": {
        "@base": ns,
        "a": "@type",
        "uri": "@id",
        "vivo": "http://vivoweb.org/ontology/core#",
        "vcard": "http://www.w3.org/2006/vcard/ns#",
        "obo": "http://purl.obolibrary.org/obo/",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "FacultyMember": "vivo:FacultyMember",
        "label": "rdfs:label",
        "first": "vcard:givenName",
        "last": "vcard:familyName",
        "middle": "vcard:middleName",
        "title": "vcard:title",
        "contact": {
            "@id": "obo:ARG_2000028",
            "@type": "@id",
            "label": "has contact info"
        },
        # "vcard":
        #     {
        #         "@id": "vcard:Individual",
        #         "@type": "@id"
        #     },
        "vcard:Name": {
            "@id": "vcard:Name",
            "@type": "@id"
        }
    }
}

fac = []

def clean(value):
    return value.strip()

with open(sys.argv[1]) as infile:
    for count, row in enumerate(csv.DictReader(infile)):
        print row
        pid = row.get('person_ID')

        puri = 'person' + pid

        f = {}
        #URI will be person_id plus person prefix.
        f['uri'] = 'person' + pid
        f['a'] = "FacultyMember"
        f['label'] = clean(row.get('name'))

        #The name vcard.
        nuri = puri + 'name'
        #title
        turi = puri + 'title'


        #Main Vcard
        vc = {}
        vc['uri'] = puri + 'vcard'
        vc['type'] = "vcard:Individual"
        vc['contact'] = nuri

        n = {}
        n['uri'] = nuri
        n['a'] = 'vcard:Name'
        n['first'] = clean(row.get('first'))
        n['last'] = clean(row.get('last'))
        middle = row.get('middle')
        if middle != "":
            n['middle'] = middle

        #Title
        t = {}
        t['uri'] = turi
        t['a'] = "vcard:Title"
        t['title'] = clean(row.get('title'))
        vc['vc:hasTitle'] = turi

        f.update(faculty)
        n.update(faculty)
        t.update(faculty)

        fac.append(f)
        fac.append(n)
        fac.append(t)

        if count > 5:
            break


#print json.dumps(fac, indent=2)

raw_jld = json.dumps(fac)
g = Graph().parse(data=raw_jld, format='json-ld')
print g.serialize(format='n3')

# g.serialize('tmp.n3', format='n3')


