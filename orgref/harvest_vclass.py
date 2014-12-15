"""
Crawl VIVO sites by Class group.
https://wiki.duraspace.org/display/VIVO/VIVO+Glossary

$ python harvest_resources.py --url http://vivo.cornell.edu/ --vclass http://vivoweb.org/ontology/core#GraduateStudent

"""


import sys
from urllib import quote

from rdflib import Graph, URIRef, XSD, Namespace
from rdflib.namespace import DCTERMS, SKOS, FOAF, RDF, RDFS

import requests
requests.packages.urllib3.disable_warnings()
#Cache if we can
try:
    import requests_cache
    requests_cache.install_cache('./data/vivocrawling')
except ImportError:
    pass

import click

from common import cached_graph

def get_resources(base_url, vclass, handle_https=False, limit=None, delay=None):
    """
    Returns an RDFLib Graph.
    """
    url = base_url.strip('/') + '/listrdf?vclass=' + quote(vclass)
    print>>sys.stderr, "Getting class", url
    vclass_obj = URIRef(vclass)

    g = cached_graph(url)
    print>>sys.stderr, "Resources found", len(g)

    #Load info about each Univ found.
    out_g = Graph()
    for count, uri in enumerate(
            g.subjects(predicate=RDF.type, object=vclass_obj)
            ):
        print>>sys.stderr, "Fetching", uri
        #Get the graph from the resource URL.
        if handle_https is True:
            uri = uri.replace('http', 'https')
        orgg = cached_graph(uri, delay=delay)
        #Continue if we can't load the resource.
        if orgg is None:
            continue
        out_g += orgg
        if (limit is not None) and (count >= limit):
            break
    return out_g

@click.command()
@click.option('--url', help='VIVO site URL')
@click.option('--https', default=False, help='Handle https.')
@click.option('--vclass', default="http://vivoweb.org/ontology/core#University", help='VIVO class URI.')
@click.option('--output', default="nt", help='RDF serialized as.')
@click.option('--limit', default=None, help='Limit crawl to X urls.')
@click.option('--destination', default=None, help='File to serialize graph to.')


def harvest(url, vclass, https, output, limit, destination):
    """
    Run the harvest
    """
    g = get_resources(
        url,
        vclass,
        handle_https=https,
        limit=limit
    )
    if destination is None:
        print g.serialize(format=output)
    else:
        g.serialize(format=output, destination=destination)

if __name__ == '__main__':
    harvest()
