'''
Takes an excel-generated CSV file of insurance companies 
and possible search queries and writes it to the app Database
'''
import argparse, os, sys, csv

# Path magic, need the models and configs from elsewhere
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
from models import Base, Company, SearchOption
from config.database import database_URI

parser = argparse.ArgumentParser(prog='populate_database')
parser.add_argument('csv_source', help='the excel-exported csv for building the database')
args = parser.parse_args()

def main(csv_filepath):
    '''Iterate over lines of a CSV, parsing records and insterting them into a database'''
    for row, record in enumerate(csv_parselines(csv_filepath)):
        pass # Insert into database

def csv_parselines(csv_filepath):
    '''Yield parsed CSV lines one at a time'''
    with open(csv_filepath, 'r') as csv_file:
       reader = csv.reader(csv_file, dialect='excel')
       next(reader) # Skip headings
       for record in reader:
           yield parse_line(record)

def parse_record(record):
    '''Parse a single line from a CSV'''
    return {'company':row[0], 'payer_id':row[1].upper(), 'search_options':_parse_search_options(row)}

if __name__ == '__main__':
    main(args.csv_source)
