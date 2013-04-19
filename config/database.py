'''Configuration settings for the database'''
from config.application import APP_ROOT

# See http://docs.sqlalchemy.org/en/rel_0_8/core/engines.html for more information
database_URI = 'sqlite:///{APP_ROOT}/db/search_database.sqlite'.format(APP_ROOT=APP_ROOT)
