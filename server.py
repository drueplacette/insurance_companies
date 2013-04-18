'''API server, returns search options for a company when company name is given.'''
import argparse, bottle, os
from bottle.ext import sqlalchemy
import filters, config
from models import Base, Company, SearchOption
from errors import NoCompanyNameError, NoPayerIDError

# Argument Parser Setup
parser = argparse.ArgumentParser(description='Serve requests for search options by insurance company name')
parser.add_argument('-s', '--server', help='hostname to run the server on', default='0.0.0.0')
parser.add_argument('-o', '--port', help='port to run the server on', type=int, default=int(os.environ.get('PORT', 5000)))
args = parser.parse_args()

# Database Setup
engine = create_engine(config.database.database_URI, echo=True)

# Bottle App Setup
app = bottle.Bottle()
app.router.add_filter('urlencode', filters.urlencode)
app.router.add_filter('uppercase', filters.uppercase)
app_db = sqlalchemy.Plugin(
    engine,
    Base.metadata,
    keyword='db',
    create=True,
    commit=True,
    use_kwargs=False
)
app.install(app_db) # plugin passes db session to any route with a 'db' argument  

# Routing
@app.get('/search/options/name/<company_name:urlencode>')
def search_options_by_company(company_name, db):
    '''Retrieve and respond with the search options for a given company name, or empty JSON if no such company exists'''
    try:
        company_id = _get_company_id_by_name(db, company_name)
        search_options = _remove_empty_fields(_get_company_search_options(db, company_id))
        search_options = _dictify_by_first([option for option in search_options if option != []])
        return {'search_options': search_options}
    except NoCompanyNameError as e:
        return e.json_error

@app.get('/search/options/id/<payer_id:uppercase>')
def search_options_by_company_id(payer_id, db):
    '''Retrieve and respond with the search options for a given company payer_id, or an error if no such company exists'''
    try:
        company_id = _get_company_id_by_payer_id(db, payer_id)
        search_options = _remove_empty_fields(_get_company_search_options(db, company_id))
        search_options = _dictify_by_first([option for option in search_options if option != []])
        return {'search_options': search_options}
    except NoPayerIDError as e:
        return e.json_error

@app.get('/lookup/companies/<search_str:urlencode>')
def search_companies(search_str, db):
    '''Search for a valid company name using an incomplete string'''
    return {'matches': _search_company_names(db, search_str)}
