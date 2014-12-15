"""
Merge two CSVs with matching idenfitiers in the first column.

Will output the second column from each file as CSV to stdout.

"""
import click
import csv
import sys
from collections import defaultdict

def read_f2(vivo):
    with open(vivo) as inf:
        d = defaultdict(list)
        for row in csv.reader(inf):
            d[row[0]].append(row[1].replace('"', ''))
    return d


def read_f1(idm):
    d = {}
    with open(idm) as infile:
        for row in csv.reader(infile):
            d[row[0]] = row[1].replace('"', '')
    return d


@click.command()
@click.option('--f1', help='CSV with ID in column 1 and some other ID in column 2')
@click.option('--f2', help='CSV with ID and VIVO url')
def main(f1, f2):
    file_1_dict = read_f1(f1)
    file_2_dict = read_f2(f2)

    first_set = set(file_1_dict.keys())
    second_set = set(file_2_dict.keys())
    matches = first_set.intersection(second_set)

    matchwriter = csv.writer(sys.stdout)
    matchwriter.writerow(['uri', 'uri2'])
    for oid in matches:
        vuris = file_2_dict[oid]
        for uri in vuris:
            matchwriter.writerow([uri, file_1_dict[oid]])

if __name__ == '__main__':
    main()