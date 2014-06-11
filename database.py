from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData
import config
import os

# XXX A very kludgy way of getting access to a database.
# This file should refactored for readability and maintainability when
# it has actually been proven to work.

# We're using the receipe suggested in 
# http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_Python.rds.html

def rds_connect_string(dbcfg):
    db_uri  = dbcfg['ENGINE'] + "://"
    db_uri += dbcfg['USER'] + ":" +  dbcfg['PASSWORD']
    db_uri += '@' + dbcfg['HOST'] + ':' + dbcfg['PORT']
    db_uri += '/' + dbcfg['NAME']
    return db_uri


def get_database_params_from_EBS_envir_params(environ):
    if 'RDS_HOSTNAME' in environ:
        DATABASES = {
            'default': {
                'ENGINE': 'postgresql',
                'NAME': environ['RDS_DB_NAME'],
                'USER': environ['RDS_USERNAME'],
                'PASSWORD': environ['RDS_PASSWORD'],
                'HOST': environ['RDS_HOSTNAME'],
                'PORT': environ['RDS_PORT'],
                }
            }
        return DATABASES
    else:
        return {}


# Then we do our thing to pick up connect params from 
# various places
DATABASES=get_database_params_from_EBS_envir_params(os.environ)

db_uri=""
if DATABASES:
    selected_db='default'
    dbcfg=DATABASES[selected_db]
    # XXX Monkeypatch due to brain damage in EBS config.
    dbcfg['PASSWORD'] = 'foobarzz'
    dbcfg['NAME'] = 'ctlmeta'

    db_uri = rds_connect_string(dbcfg)
else:
    try:
        db_uri = os.environ["SQLALCHEMY_DATABASE_URI"]
        print "Found environment variable"
    except KeyError:
        print "Did not find environment variable"
        db_uri = config.SQLALCHEMY_DATABASE_URI

print "db_uri = ", db_uri

# At this point we should have a non-empty db_uri, or else we're screwed.
if (db_uri == ""):
    raise RuntimeError("Could not determine database connect string.")

# Change to True to print all SQL statements going into and coming out of the database.
echo=False
engine = create_engine(db_uri, echo=echo)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)

def commit_db():
    try:
        db_session.commit()
    except Exception as e:
        print "database.py::commit_db():exception ", e
        raise


