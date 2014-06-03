
import csv
import hashlib
import os
import urllib

import logging
logger = logging.getLogger(__name__)

from rdflib import Graph, Namespace
from rdflib.namespace import NamespaceManager, ClosedNamespace

VIVO = Namespace('http://vivoweb.org/ontology/core#')
#FOAF = Namespace('http://xmlns.com/foaf/0.1/')
BIBO = Namespace('http://purl.org/ontology/bibo/')
OBO = Namespace('http://purl.obolibrary.org/obo/')
#SCHEMA = Namespace('http://schema.org/')
#SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
VCARD = Namespace('http://www.w3.org/2006/vcard/ns#')

namespaces = {}
for k, o in vars().items():
    if isinstance(o, (Namespace, ClosedNamespace)):
        namespaces[k] = o

ns_mgr = NamespaceManager(Graph())
for k, v in namespaces.items():
    ns_mgr.bind(k.lower(), v)



#Use when a named graph isn't specified for SPARQL update.
DEFAULT_GRAPH = 'http://vitro.mannlib.cornell.edu/default/vitro-kb-2'

def _env(name):
    val = os.getenv(name)
    if val is None:
        raise Exception("Can't find {}.  Set environment variable.".format(name))
    return val

class VUpdate(object):
    """
    VIVO SPARQL Update class
    """
    def __init__(self):
        self.endpoint = _env('VIVO_UPDATE_ENDPOINT')
        self.email = _env('VIVO_EMAIL')
        self.password = _env('VIVO_PASSWORD')

    def add(self, graph, name=None):
        """
        See:
        https://github.com/RDFLib/rdflib/blob/master/rdflib/plugins/stores/sparqlstore.py#L451
        """
        nameg = name or DEFAULT_GRAPH
        data = ""
        for subject, predicate, obj in graph:
            triple = "%s %s %s .\n" % (subject.n3(), predicate.n3(), obj.n3())
            data += triple
        sparql = "INSERT DATA \n { GRAPH <%s> {\n %s }\n}" % (nameg, data)
        self.do_update(sparql)

    def remove(self, graph, name=None):
        nameg = name or DEFAULT_GRAPH
        data = ""
        for subject, predicate, obj in graph:
            triple = "%s %s %s .\n" % (subject.n3(), predicate.n3(), obj.n3())
            data += triple
        sparql = "DELETE DATA \n { GRAPH <%s> { %s }\n}" % (nameg, data)
        self.do_update(sparql)

    def do_update(self, query):
        logger.debug('Update query:\n {}'.format(query))
        payload = {
            'email': self.email,
            'password': self.password,
            'update': query
        }
        data = urllib.urlencode(payload)
        response = urllib.urlopen(self.endpoint, data)
        #This will raise an expection if something goes wrong
        if response.code != 200:
            raise Exception("SPARQL update failed.  Status code: {}".format(str(response.code)))
        #Verify that we actually hit the API endpoint.  This is hardcoded.  Should read 
        #from properties or something.
        if 'api/sparqlUpdate' not in response.url:
            raise Exception("Response URL doesn't seem to be the VIVO API URL.  Verify settings.")
        logger.info("Update response code: {}".format(response.code))
        return True

def hash_uri(raw, prefix='n'):
    """
    Return a hash of the next in numerical form.

    Prefix with the prefix text.
    """
    hobj = hashlib.md5(raw)
    return prefix + hobj.hexdigest()

def scrub_row(row):
    """
    Set values that are empty strings - "" -
    to Python None.

    Remove carriage returns and line breaks from cells.  Encode
    as utf-8.
    """
    out_dictionary = {}
    for k,v in row.items():
        #Remove line breaks and carriage returns.
        v = v.replace('\n', '').replace('\r', '')
        if v == '':
            out_dictionary[k] = None
        else:
            out_dictionary[k] = v.decode('utf-8', 'ignore')
    return out_dictionary

def read_file(file_name, delimiter=','):
    """
    Read in the file and clean the rows.
    """
    out = []
    with open(file_name) as infile:
        for row in csv.DictReader(infile, delimiter=delimiter):
            clean_row = scrub_row(row)
            out.append(clean_row)
    return out