"""
Example DOI to VIVO publication script.
"""

import sys

from rdflib import Graph, Namespace, Literal, RDF, RDFS
from utils import crossref_metadata_search, hash_uri
from utils import BIBO, VIVO

from utils import VUpdate
vstore = VUpdate()

D = Namespace('http://vivo.school.edu/individual/')

def get(doi):
    meta = crossref_metadata_search(doi)
    return meta[0]

def map_pub(doi, meta, author_uri):
    g = Graph()

    author_uri = D[author_uri] #URIRef(author_uri)

    pub_local_name = hash_uri('pub' + doi + author_uri)
    publication_uri = D[pub_local_name]
    #pub metadata
    g.add( (publication_uri, RDF.type, BIBO.Document) )
    g.add( (publication_uri, RDFS.label, Literal(meta['title'])) )
    g.add( (publication_uri, BIBO.doi, Literal(doi)) )

    #authorhsip uri - create hash of these strings.
    local_name = hash_uri('aship' + doi + author_uri)
    authorship_uri = D[local_name]
    g.add( (authorship_uri, RDF.type, VIVO.Authorship) )
    g.add( (authorship_uri, VIVO.relates, publication_uri) )
    g.add( (authorship_uri, VIVO.relates, author_uri) )

    return g

def load(graph):
    vstore.add(g)
    return True

if __name__ == "__main__":
    faculty_local_name = sys.argv[1]
    doi = sys.argv[2]
    meta = get(doi)
    print doi
    print
    g = map_pub(doi, meta, faculty_local_name)

    print load(g)
