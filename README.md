Insurance Companies - Search Option Queries
===========================================
Web services to retrieve search information by insurance company.

Setting Up
----------
**This API server requires Python 3.0+.**


First off, install the requirements (creating a virtualenv first if you wish):
```bash
$ pip install -r requirements.txt
```

Next you need to populate the database. To do this you'll need to export a CSV file from the Search Options by Insurance Company excel spreadsheet. After that's done, execute the population script:
```bash
$ python bin/populate_database.py <path-to-csv-file>
```

After that, start the api server. The default host and port are 0.0.0.0 and 5000 - you can specify different ones using the -s and -p options. If the environment has a PORT env variable set, that will be the default if none is specified by the user.
```bash
$ python server.py
```

By default the port the server binds to is taken from env["PORT"], or if there is no such env variable, port 5000. In the general use case, the server will bind tolocalhost:5000. You can also specify hostname and database for the server. Call up its help to view the options for these.

Supported Requests
------------------
The API server responds to two types of requests: search options requests and company search requests.

**Search Options and Company Lookups**

These routes are currently avalaible:
For retrieving search options:
* `/searchoptions/name/<company_name>`
* `/searchoptions/id/<payer_id>`

For looking up companies:
* `/company/name/<partial_name>`
* `/company/id/<partial_id>`

Updating the Database
---------------------
Currently no proper way of doing this is included; for the time being, the only other option is to rebuild the database and then replace the old with the new. Don't re-write onto the old database, as you'll end up with dupicated copies of everything.

Configuration
-------------
...(for the moment, look in config/*.py)

Bundled Scripts
---------------
**bin/populate_database.py**

Takes an excel-generated CSV file of the insurance companies and uses it to populate the database specified in the config.

Usage:
```bash
$ cd scripts
$ python build_db.py <input_csv_file>
```
