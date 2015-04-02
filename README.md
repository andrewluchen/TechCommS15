# Compile My Style

### By Andrew Chen, Patrick Yurky, Joey Fernau, Sally McNichols

Compile My Style will be a web application with the purpose of helping its users to make better fashion decisions.  Knowledge of clothing and style is an area where people tend to have either a great deal of knowledge or almost none.  Most people today are not involved in the world of fashion, and many people never have the opportunity to learn what clothing styles they like or for which they are well-suited.  There are currently not any many sources from which people can gain this knowledge other than direct interaction with others.  Our hope is to bring these two groups together so that those with knowledge of fashion and clothing styles can share their expertise with those without such knowledge.  We aim to replicate the type of teaching and and fashion assistance that currently can only be achieved by in-person interactions.


## Setup & Installation

* Flask 0.10.1 (`pip install flask`)
* Flask-Login 0.2.11 (`pip install flask-login`)
* Flask-OAuth 0.12 (`pip install flask-oauth`)
* Flask-SQLAlchemy 2.0 (`pip install flask-sqlalchemy`)
* PostgreSQL (`apt-get install postgresql`)
* psycopg2 2.5.3 (`pip install psycopg2`)
* dropbox 2.2.0 (`pip install dropbox`)
* *Werkzeug 0.9.6 (`pip install Werkzeug==0.9.6`)


### Notes about installation

Only install Werkzeug 0.9.6 if there is an error. On some computers, Werkzeug 0.10.4 stat seems to cause `ImportError: No module named _winreg` with dropbox 2.2.0


## Build Instructions

To build:
```bash
$ git clone git@github.com:smcnichols/TechCommS15.git
$ cd TechCommS15
$ heroku pg:pull HEROKU_POSTGRESQL_GRAY your_local_database_name_here
$ python app.py
```
