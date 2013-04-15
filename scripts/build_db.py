'''
Takes an excel-generated CSV file of insurance companies 
and possible search queries and writes it to an SQLite Database
'''
import sys
import csv, sqlite3

def main(csv_in, sqlite_out):
    '''Iterates over a CSV file, parsing each line and inserting it into the database'''
    conn = sqlite3.connect(sqlite_out)

    try:
        for row, record in enumerate(csv_parselines(csv_in)):
            _clear_line()
            db_insert_records(conn, record)
            print(row, "rows inserted.", sep="")

        print("\nCommiting changes...")
        conn.commit()
        print("done")
    finally:
        conn.close() # Failsafe, ensure connection closes.
        
def csv_parselines(filepath):
    '''A generator, which parses the csv a line at a time, returning records ready to read into the database'''
    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, dialect='excel')
        next(csv_reader) # Skip headings
        for row in csv_reader:
            yield parse_records(row)

def parse_records(row):
    '''Takes a flat list and returns a dictionary containing the company name and a list of numbered options'''
    return {'company':row[0], 'search_options':_parse_search_options(row)}

def db_insert_records(db_conn, parsed_records):
    '''Inserts parsed records into the database'''
    db_cursor = db_conn.cursor()

    # Insert Company Name
    db_cursor.execute('INSERT INTO company VALUES (NULL, ?)', [parsed_records['company']])
    # Retrieve Company ID
    company_id = db_cursor.lastrowid
    # Add search options
    for search_option in parsed_records['search_options']:
        if len(search_option) < 7:
            search_option += ['']*(7-len(search_option)) # Pad empty search terms
        db_cursor.execute('''INSERT INTO search VALUES (NULL, ?,?,?,?,?,?,?,?)''', 
                        [company_id] + search_option)

def _parse_search_options(row):
    '''Parse the search options for a specific row, returning a list of options (list of lists of fields)'''
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

def _clear_line():
    '''Write a carriage return character to stdout'''
    sys.stdout.write("\r")
    sys.stdout.flush()

if __name__ == '__main__':
    main(csv_in=sys.argv[1], sqlite_out=sys.argv[2]) # Placeholder until proper argparse put in place
