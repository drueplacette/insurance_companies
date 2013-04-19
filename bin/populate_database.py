'''
Takes an excel-generated CSV file of insurance companies 
and possible search queries and writes it to the app Database
'''
import argparse, os

parser = argparse.ArgumentParser(prog='populate_database')
parser.add_argument('csv_source', help='the excel-exported csv for building the database')
parser.add_argument('-d', help='URI of the database', default=os.environ.get("DATABASE_URI"))
args = parser.parse_args()

def main():
    '''Iterate over lines of a CSV, parsing records and insterting them into a database'''
    pass

def csv_parselines(csvfile):
    '''Yield parsed CSV lines one at a time'''
    pass

def parse_line(line):
    '''Parse a single line from a CSV'''
    pass
