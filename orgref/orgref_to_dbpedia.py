"""
Outputs CSV to stdout with the OrgRef ID in the first column
and the DBPedia URI in the second.  E.g.

orgref-id,uri
1859,http://dbpedia.org/resource/Arizona_State_University
2025,http://dbpedia.org/resource/Crandall_University

This script is expecting the user to download the Wikipedia page IDs
from DBpedia as ntriples.

http://wiki.dbpedia.org/Downloads2014

$ python orgref_to_dbpedia.py --orgref orgref.csv --dbpedia page_ids_en.nt

"""

import click
import sys
import csv

from rdflib import Graph, Namespace

DBP = Namespace('http://dbpedia.org/ontology/')

from common import read_oref_csv

def process_dbpedia(dbpedia, orgref_ids):
    with open(dbpedia) as infile:
        print>>sys.stderr, "DBP graph read."
        #skip first line
        infile.next()
        for count, row in enumerate(infile):
            if (count > 0) and (count % 1000000 == 0):
                print>>sys.stderr, count, "read."
            g = Graph().parse(data=row, format='nt')
            for sub, obj in g.subject_objects(predicate=DBP.wikiPageID):
                wikid = unicode(obj.toPython())
                if wikid in orgref_ids:
                    yield (wikid, sub.toPython())

def process_orgref(orgref):
    ids = set()
    for row in read_oref_csv(orgref):
        #If an orgref row doesn't have a wikipedia URL, then
        #the ID is not a Wikipedia page ID.
        wiki_url = row.Wikipedia
        if wiki_url is None:
            continue
        else:
            ids.add(row.ID)
    return ids

@click.command()
@click.option('--orgref', help='OrgRef CSV')
@click.option('--dbpedia', help='DBPedia to Wikipedia IDs')

def match(orgref, dbpedia):
    """
    Run the match
    """
    oref_ids = process_orgref(orgref)
    print>>sys.stderr, "OrgRef set created."
    dbp_pairs = process_dbpedia(dbpedia, oref_ids)

    matchwriter = csv.writer(sys.stdout)
    matchwriter.writerow(['orgref-id', 'uri'])
    for a, b in dbp_pairs:
        matchwriter.writerow([a, b])

if __name__ == '__main__':
    match()