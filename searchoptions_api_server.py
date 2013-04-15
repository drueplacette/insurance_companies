'''API server, returns search options for a company when company name is given.'''
import argparse, sqlite3
from bottle import Bottle, route, run
from urlencode_filter import urlencode_filter

# Argument Parser Setup
parser = argparse.ArgumentParser(description='Serve requests for search options by insurance company name')
parser.add_argument('-s', '--server', help='hostname to run the server on', default='0.0.0.0')
parser.add_argument('-o', '--port', help='port to run the server on', type=int, default='5000')
parser.add_argument('-d', '--database', help='SQLite database file to use', default='db/search_database.sqlite')
args = parser.parse_args()

# Setup
app = Bottle()
app.router.add_filter('urlencode', urlencode_filter)

# Routing
@app.route('/search/options/<company_name:urlencode>')
def search_options_by_company(company_name):
    '''Retrieve and respond with the search options for a given company name, or empty JSON if no such company exists'''

    database = args.database
    with SQLiteDatabaseConnection(database) as conn:
        company_id = _get_company_id(conn, company_name)
        if company_id is None:
            return {}

        search_options = _remove_empty_fields(_get_company_search_options(conn, company_id))

    search_options = _dictify_by_first([option for option in search_options if option != []])
    return {'search-options': search_options}

@app.route('/search/companies/<search_str:urlencode>')
def search_companies(search_str):
    '''Search for a valid company name using an incomplete string'''
    
    database = args.database
    with SQLiteDatabaseConnection(database) as conn:
        return {"matches":_search_company_names(conn, search_str)}

# Helper functions
def _get_company_id(conn, company_name):
    '''Return company id given company name'''
    c = conn.cursor()
    c.execute('SELECT ROWID FROM company WHERE name=?', [company_name])
    company_id = c.fetchone()

    return company_id[0] if company_id else None # Unpack returned value

def _get_company_search_options(conn, company_id):
    '''Return search options given company id'''
    c = conn.cursor()
    c.execute('''SELECT searchoption, field1, field2, field3, field4, field5, field6
                 FROM search
                 WHERE searchcompany=?''', [company_id])
    return c.fetchall()

def _search_company_names(conn, search_str):
    '''Perform a search for a company name given a partially complete string, and return possible matches as JSON'''
    c = conn.cursor()
    c.execute('SELECT name FROM company WHERE name LIKE ?', ['%' + search_str + '%'])
    return [_flatten_result(result) for result in c.fetchall()]

def _flatten_result(result):
    '''Flatten a search result from a SELECT statement where only one value is returned'''
    return result[0]

def _remove_empty_fields(search_options):
    '''Remove any empty fields from a search option'''
    return [[field for field in option if field != ''] for option in search_options]

def _dictify_by_first(search_options):
    '''Convert a flat list of search options into a dict mapping option numbers to their option arguments'''
    search_dict = {}
    for option in search_options:
        search_dict[option[0]] = option[1:] # First item of option as key, rest as value list

    return search_dict

class SQLiteDatabaseConnection(object):
    '''Provides an object for opening and using an SQLite Database with python's 'with' syntax'''
    def __init__(self, database):
        self.database = database

    def __enter__(self):
        self._connection = sqlite3.connect(self.database)
        return self._connection

    def __exit__(self, type, value, traceback):
        self._connection.close()
        print(type, value, traceback)


if __name__ == '__main__':
    app.run(host=args.server, port=args.port)
