'''
Takes an excel-generated CSV file of insurance companies 
and possible search queries and writes it to the app Database
'''
import argparse, os, sys, csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Path magic, need the models and configs from elsewhere
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
from models import * # Required for automated db builds
from config.database import database_URI

parser = argparse.ArgumentParser(prog='populate_database')
parser.add_argument('csv_source', help='the excel-exported csv for building the database')
args = parser.parse_args()

def main(csv_filepath):
    '''Iterate over lines of a CSV, parsing records and insterting them into a database'''
    engine = create_engine(database_URI, echo=False)
    Base.metadata.create_all(engine) # Create tables if they don't exist
    Session = sessionmaker(bind=engine)
    session = Session()

    for row, record in enumerate(csv_parselines(csv_filepath)):
        clear_line()
        print(row, 'rows inserted...', end=' ')
        company = Company(record['name'], record['payer_id'])
        session.add(company)
        session.commit() # Commits the company record to the db,
                         # and more importantly, updates the company object with its new id
        for option in record['search_options']:
            search_option = SearchOption(company.id, *option)
            session.add(search_option)
        session.commit()

    print 'done'

def csv_parselines(csv_filepath):
    '''Yield parsed CSV lines one at a time'''
    with open(csv_filepath, 'r') as csv_file:
       reader = csv.reader(csv_file, dialect='excel')
       next(reader) # Skip headings
       for row in reader:
           yield parse_record(row)

def parse_record(row):
    '''Parse a single line from a CSV'''
    return {'name':row[0], 'payer_id':row[1].upper(), 'search_options':parse_search_options(row)}

def parse_search_options(row):
    '''Parse the search options for a specific row, returning a list of options (list of lists of fields)'''
    # fallback approach due to uneven field sizes. Messy.
    search_options = [row[3:7], row[9:14]] + [row[(i*6)+15+1:(i*6)+15+6] for i in range(9)]
    # Remove empty fields from options
    search_options = [[field for field in option if field != ''] 
                        for option in search_options]
    # Number options and remove empty options
    search_options = [option for option in enumerate(search_options, start=1)
                        if ''.join(option[1]) != '']
    # Flatten option number into list
    search_options = [[option[0]] + option[1] for option in search_options]
    return search_options

def clear_line():
    '''Write a carriage return character to stdout'''
    sys.stdout.write("\r")
    sys.stdout.flush()

if __name__ == '__main__':
    main(args.csv_source)
