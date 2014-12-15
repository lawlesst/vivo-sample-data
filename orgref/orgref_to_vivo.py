import csv
from collections import defaultdict
import sys

import click
from rdflib import Graph

from common import text_normalize

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


def process_orgref(fname):
    out = defaultdict(list)
    for count, row in enumerate(read_oref_csv(fname)):
        clean_name = text_normalize(row.Name)
        out[clean_name].append(row.ID)
    return out


def process_vivo(graph_filename, vclass, format):
    g = Graph()
    g.parse(graph_filename, format=format)
    rq = """
    SELECT DISTINCT ?org ?label
    WHERE
    {
          ?org a VCLASS .
          ?org rdfs:label ?label .
    }
    """.replace('VCLASS', '<{}>'.format(vclass))
    out = defaultdict(list)
    for org, label in g.query(rq):
        nl = text_normalize(label.toPython())
        out[nl].append(org.toPython())
    return out


@click.command()
@click.option('--orgref', help='OrgRef CSV')
@click.option('--vivo', help='VIVO site file')
@click.option('--vclass', default="http://vivoweb.org/ontology/core#University", help='VIVO class URI.')
@click.option('--format', default="nt", help='RDF serialized as.')

def match(orgref, vivo, vclass, format):
    """
    Run the match
    """
    oref = process_orgref(orgref)
    vivo = process_vivo(vivo, vclass, format)

    matchwriter = csv.writer(sys.stdout)
    matchwriter.writerow(['orgref-id', 'uri'])
    for orlabel, orefid in oref.items():
        matched = vivo.get(orlabel, [])
        for vid in matched:
            for oid in orefid:
                matchwriter.writerow([oid, vid])

if __name__ == '__main__':
    match()