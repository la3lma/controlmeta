from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData
import config
import os

# A very kludgy way of getting access to a database.
# (refactor when shown to actually work)
# First se see if there is an Amazon RDS instance available.
# We're using the receipe suggested in 
# http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_Python.rds.html

def rds_connect_string(dbcfg):
    db_uri  = dbcfg['ENGINE'] + "://"
    db_uri += dbcfg['RDS_USERNAME'] + ":" +  dbcfg['RDS_PASSWORD']
    db_uri += '@' + dbcfg['RDS_HOSTNAME'] + ':' + dbcfg['RDS_PORT']
    db_uri += '/' + dbcfg['RDS_DB_NAME']
    return db_uri

if 'RDS_HOSTNAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'postgresql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
    selected_db='default'
    dbcfg=DATABASES[selected_db]
    db_uri = rds_connect_string(dbcfg)

else:
    try:
        db_uri = os.environ["SQLALCHEMY_DATABASE_URI"]
        print "Found environment variable"
    except KeyError:
        print "Did not find environment variable"
        db_uri = config.SQLALCHEMY_DATABASE_URI

# Change to true to print all SQL statements going into and coming out of the database.
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


