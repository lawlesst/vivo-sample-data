"""
Load the people.csv file as VIVO Faculty Members.

See VCard usage:
https://wiki.duraspace.org/display/VIVO/VCard+usage+diagram

"""

import csv
import json
import sys

import logging
logging.basicConfig(level=logging.INFO)

from rdflib import Graph
from rdflib_jsonld.parser import to_rdf
from utils import ns_mgr

#Data namespace
ns = "http://vivo.school.edu/individual/"

faculty_ctx = {
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
        "middle": "vivo:middleName",
        "title": "vcard:title",
        "contact": {
            "@id": "obo:ARG_2000028",
            "@type": "@id",
            "label": "has contact info"
        },
        "vcard:hasName":
            {
            "@id": "vcard:hasName",
            "@type": "@id"
        },
        "vcard:hasTitle":
            {
            "@id": "vcard:hasTitle",
            "@type": "@id"
        },
        "hasEmail":
            {
            "@id": "vcard:hasEmail",
            "@type": "@id"
        },
        "hasPhone":
            {
            "@id": "vcard:hasTelephone",
            "@type": "@id"
        },
        "telephone": "vcard:telephone",
    }
}

fac = []

with open(sys.argv[1]) as infile:
    for count, row in enumerate(csv.DictReader(infile)):
        pid = row.get('person_ID')

        faculty_uri = 'fac' + pid

        #Our faculty dictionary
        f = {}

        #URI will be person_id plus person prefix.
        f['uri'] = faculty_uri
        f['a'] = "FacultyMember"
        f['label'] = row.get('name').strip()
        f.update(faculty_ctx)
        fac.append(f)

        #Individual vcard
        vcard_uri = faculty_uri + '-vcard'
        f['contact'] = vcard_uri
        #Name vcard.
        vcard_name_uri = faculty_uri + '-vcard-name'
        #Title vcard
        vcard_title_uri = faculty_uri + '-vcard-title'
        #Email vcard
        vcard_email_uri = faculty_uri + '-vcard-email'
        #Phone
        vcard_phone_uri = faculty_uri + '-vcard-phone'
        #Fax
        vcard_fax_uri = faculty_uri + '-vcard-fax'


        #Main Vcard
        vc = {}
        vc['uri'] = vcard_uri
        vc['a'] = 'vcard:Individual'
        vc['vcard:hasName'] = vcard_name_uri
        vc.update(faculty_ctx)
        fac.append(vc)

        n = {}
        n['uri'] = vcard_name_uri
        n['a'] = 'vcard:Name'
        n['first'] = row.get('first')
        n['last'] = row.get('last')
        middle = row.get('middle')
        if middle != "":
            n['middle'] = middle
        n.update(faculty_ctx)
        fac.append(n)

        #Title
        t = {}
        t['uri'] = vcard_title_uri
        t['a'] = "vcard:Title"
        t['title'] = row.get('title')
        vc['vcard:hasTitle'] = vcard_title_uri
        t.update(faculty_ctx)
        fac.append(t)

        #Email
        email = row.get('email')
        if email != '':
            e = {}
            e['a'] = ["vcard:Email", "vcard:Work"]
            e['uri'] = vcard_email_uri
            e['vcard:email'] = email
            e.update(faculty_ctx)
            vc['hasEmail'] = vcard_email_uri
            fac.append(e)

        #Phone
        phone = row.get('phone')
        if phone != '':
            p = {}
            p['uri'] = vcard_phone_uri
            p['a'] = ["vcard:Telephone", "vcard:Work", "vcard:Voice"]
            p['telephone'] = phone
            p.update(faculty_ctx)
            fac.append(p)

        #Fax - really, 2014.
        fax = row.get('fax')
        if fax != '':
            f = {}
            f['uri'] = vcard_fax_uri
            f['a'] = ["vcard:Telephone", "vcard:Work", "vcard:Fax"]
            f['telephone'] = fax
            f.update(faculty_ctx)
            fac.append(f)

        vc['hasPhone'] = [vcard_phone_uri, vcard_fax_uri]


g = Graph()
g.namespace_manager = ns_mgr
out = to_rdf(fac, g)
print out.serialize(format='turtle')


