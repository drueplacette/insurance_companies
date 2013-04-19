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
    conn = engine.connect()
    transaction = conn.begin()

    company_table = Company.__table__
    search_option_table = SearchOption.__table__

    for row, record in enumerate(csv_parselines(csv_filepath)):
        clear_line()
        print(row, 'rows inserted...', end=' ')
        company = company_table.insert().values(name=record['name'], payer_id=record['payer_id'])
        key = conn.execute(company) # Need this for associating the
                                    # search options with the company

        for option in record['search_options']:
            if len(option) < 7:
                option += ['']*(7-len(option)) # pad out empty fields

            # Unfortunately, this is quite dirty due to the schema...
            # Fully normalising the schema would make this look better,
            # but require more models to be made, wouldn't be
            # very efficient in terms of data.
            search_option = search_option_table.insert().values(
                                company_id=key.lastrowid, option_number=option[0],
                                field1=option[1], field2=option[2], field3=option[3],
                                field4=option[4], field5=option[5], field6=option[6])
            conn.execute(search_option)
                
    print('commiting')
    transaction.commit()
    print('done')

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
