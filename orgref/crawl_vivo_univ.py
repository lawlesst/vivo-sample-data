"""
Example of crawling multiple VIVO sites for data
about universities.  Outputs ntriples.

Will issue one request per second to each VIVO.

"""

from urlparse import urlparse
import harvest_vclass

sites = [
    #{'url': 'https://vivo.health.unm.edu/', 'https': True},
    #{'url': 'https://vivo.brown.edu/', 'https': True, 'vclass': 'http://xmlns.com/foaf/0.1/Organization'},
    #{'url':'https://scholars.duke.edu/'},
    #{'url':'http://vivo.ufl.edu/'},
    #{'url':'http://vivo.cornell.edu/'},
    #{'url':'http://vivo.med.cornell.edu/'},
    {'url':'http://vivo.nkn.uidaho.edu/vivo/'},
    #Deep carbon not working at moment.
    #{'url':'https://info.deepcarbon.net/vivo/', 'https':False},
    {'url':'https://vivo.apa.org/', 'https':True}
]


#def harvest(url, vclass, https, output, limit, destination):
def grab():
    vclass = 'http://vivoweb.org/ontology/core#University'
    limit = None
    for site in sites:
        url = site['url']
        https = site.get('https', False)
        get_vclass = site.get('vclass', vclass)
        g = harvest_vclass.get_resources(url, get_vclass, handle_https=https, limit=limit, delay=True)
        url_name = urlparse(url)
        fname = url_name.netloc.replace('.', '_')
        print g.serialize(format='nt', destination='./data/sites/{}.nt'.format(fname))

if __name__ == '__main__':
    grab()