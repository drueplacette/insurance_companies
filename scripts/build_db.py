'''
Takes an excel-generated CSV file of insurance companies 
and possible search queries and writes it to an SQLite Database
'''
from sys import argv
import csv, sqlite3

def main(csv_in, sqlite_out):
    '''Iterates over a CSV file, parsing each line and inserting it into the database'''
    for record in csv_parselines(csv_in):
        db_insert_records(record)
        print record

def csv_parselines(filepath):
    '''A generator, which parses the csv a line at a time, returning records ready to read into the database'''
    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, dialect='excel')
        csv_reader.next() # Skip headings
        for row in csv_reader:
            yield parse_records(row)

def parse_records(row):
    '''Takes a flat list and returns a tuple containing the company name and a list of numbered options'''
    return {'company':row[0], 'search_options':_parse_search_options(row)}

def db_insert_records(parsed_records):
    '''Inserts parsed records into the database'''
    pass

def _parse_search_options(row):
    # fallback approach due to uneven field sizes. Messy.
    search_options = [row[2:6], row[8:13]] + [row[(i*6)+14+1:(i*6)+14+6] for i in range(9)]
    # Remove empty fields from options
    search_options = [[field for field in option if field != ''] 
                        for option in search_options]
    # Number options and remove empty options
    search_options = [option for option in enumerate(search_options, start=1)
                        if ''.join(option[1]) != '']
    # Flatten option number into list
    search_options = [[option[0]] + option[1] for option in search_options]

    return search_options

if __name__ == '__main__':
    main(csv_in=argv[1], sqlite_out=argv[2]) # Placeholder until proper argparse put in place
