Insurance Companies - Search Option Queries
===========================================
Web services to retrieve search information by insurance company.

Setting Up
----------
This API server requires Python 3.0+.

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
$ python searchoptions_api_server.py
```

By default the port the server binds to is taken from env["PORT"], or if there is no such env variable, port 5000. In the general use case, the server will bind tolocalhost:5000. You can also specify hostname and database for the server. Call up its help to view the options for these.

Supported Requests
------------------
The API server responds to two types of requests: search options requests and company search requests.

**Search Options**

The route for these options is `/search/options/<insurance_company_name>`. If no such company exists, an empty JSON object will be returned.
```bash
$ curl -l <server_address>/search/options/name/Aetna+Long+Term+Care
{"search_options": {"1": ["subscriber_id", "subscriber_last_name", "subscriber_first_name", "subscriber_dob"]}}

$ curl -l <server_address>/search/options/name/Invalid+Name
{"error": "No such company with name: Invalid Name"}
```
You can also search by the company's payer id.
```bash
$ curl -l <server_address>/search/options/id/CTOTL
...

$ curl -l <server_address>/search/options/id/INVALID
{"error": "No such company with payer id: INVALID"}
```


**Company Search**

The route for searching companies is `/search/companies/<search_string>`. If no companies are found, the "matches" attribute of the returned JSON object will be empty.
```bash
$ curl -l <server_address>/lookup/companies/AARP
{"matches": ["AARP"]}

$ curl -l <server_address>/lookup/companies/Invalid+Name
{"matches": []}
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
