set -e
#!/bin/bash

echo "Building RDF"

python faculty.py data/faculty.csv > rdf/faculty.ttl
python organizations.py data/organizations.csv > rdf/organizations.ttl
python positions.py data/positions.csv > rdf/positions.ttl
python combine.py > rdf/all.ttl

echo "Done"