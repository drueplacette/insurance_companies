Insurance Companies - Search Option Queries
===========================================
Web services to retrieve search information by insurance company.

Setting Up
----------
First off, install the requirements:
```bash
$ pip install -r requirements.txt
```

Create a database file in /db/. The suggested name is 'search_database.sqlite', as this is the api server's default.
```bash
$ cd db
$ cat schema.sql | sqlite3 search_database.sqlite
$ cd ..
```

Next you need to populate the database. To do this you'll need to export a CSV file from the Search Options by Insurance Company excel spreadsheet. After that's done, use scripts/build_db.py to build the database.
```bash
$ cd scripts
$ python build_db.py <path-to-csv-file> ../db/search_database.sqlite
$ cd ..
```

After that, start the api server. The default port is 8080, but you can specify a different one using the -p option
```bash
$ python searchoptions_api_server.py -p <port>
```

Updating the Database
---------------------
Currently no proper way of doing this is included; for the time being, the only other option is to rebuild the database and then replace the old with the new. Don't re-write onto the old database, as you'll end up with dupicated copies of everything.

Bundled Scripts
---------------
**scripts/build_db.py**

Takes an excel-generated CSV file of the insurance companies and possible search queries and builds an SQLite database from it.

Usage:
```bash`
$ cd scripts
$ python build_db.py <input_csv_file> <output_sqlite_file>
```
