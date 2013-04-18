'''API server, returns search options for a company when company name is given.'''
import argparse, bottle, os
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine
import filters, config
from models import Base, Company, SearchOption
from errors import NoCompanyNameError, NoPayerIDError, NoSearchResultsError

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
    create=True,  # Automatically create db and tables if they don't exist
    commit=False, # API server can't alter database
    use_kwargs=False
)
app.install(app_db) # plugin passes db session to any route with a 'db' argument  

# Routing
@app.get('/search_options/id/<payer_id:urlencode>')
def search_options_by_payer_id(payer_id, db):
    '''Find search options for a given company by payer ID'''
    try:
        company = db.query(Company).filter_by(payer_id=payer_id).first()
        if company is None:
            raise NoPayerIDError(payer_id)
        return {"search_options":[option.jsonify() for option in company.search_options]}

    except NoPayerIDError as e:
        return e.json_error

@app.get('/search_options/name/<name:urlencode>')
def search_options_by_name(name, db):
    '''Find search options for a given company by name'''
    try:
        company = db.query(Company).filter_by(name=name).first()
        if company is None:
            raise NoCompanyNameError(payer_id)
        return {"search_options":[option.jsonify() for option in company.search_options]}

    except NoCompanyNameError as e:
        return e.json_error

@app.get('/company/id/<search_id:uppercase>')
def find_company_by_payer_id(search_id, db):
    '''Search for a company by id'''
    try:
        companies = db.query(Company).filter(Company.payer_id.like('%{}%'.format(search_id))).all()
        if len(companies) == 0:
            raise NoSearchResultsError(search_id)
        return {"search_results":[company.jsonify() for company in companies]}

    except NoSearchResultsError as e:
        return e.json_error


@app.get('/company/name/<search_name:urlencode>')
def find_company_by_name(search_name, db):
    '''Search for a company by name'''
    try:
        companies = db.query(Company).filter(Company.name.like('%{}%'.format(search_name))).all()
        if len(companies) == 0:
            raise NoSearchResultsError(search_name)
        return {"search_results":[company.jsonify() for company in companies]}

    except NoSearchResultsError as e:
        return e.json_error

if __name__ == '__main__':
    app.run(host=args.server, port=args.port)
