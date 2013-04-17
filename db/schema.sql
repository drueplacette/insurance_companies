CREATE TABLE company (
id integer PRIMARY KEY,
name    text,
payerid text
);

CREATE TABLE search (
id integer PRIMARY KEY,
searchcompany integer,
searchoption integer,
field1 text,
field2 text,
field3 text,
field4 text,
field5 text,
field6 text
);
