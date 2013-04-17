CREATE TABLE companies (
id integer PRIMARY KEY,
name     string,
payer_id string
);

CREATE TABLE search_options (
id integer PRIMARY KEY,
company_id integer,
option_number integer,
field1 string,
field2 string,
field3 string,
field4 string,
field5 string,
field6 string
);
