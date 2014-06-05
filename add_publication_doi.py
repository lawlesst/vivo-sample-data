import sys

from utils import crossref_metadata_search

def get(doi):
    meta = crossref_metadata_search(doi)
    return meta[0]

if __name__ == "__main__":
    doi = sys.argv[1]
    meta = get(doi)
    print doi
    print
    print meta['title']