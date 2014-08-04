set -e
#!/bin/bash

echo "Building RDF"

CSV=data/csv
DATA_DIR=data/rdf

python people.py $CSV/people.csv > $DATA_DIR/faculty.ttl
python organizations.py $CSV/organizations.csv > $DATA_DIR/organizations.ttl
python positions.py $CSV/positions.csv > $DATA_DIR/positions.ttl
python combine.py > $DATA_DIR/all.ttl

echo "Done"