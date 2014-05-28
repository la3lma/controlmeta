from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData
import config
import os


# A kludgy way of gettingi config either from
# an environment variable (as typically done during testing)
# or from a config file (typically done during operation)

try:
    db_uri = os.environ["SQLALCHEMY_DATABASE_URI"]
    print "Found environment variable"
except KeyError:
    print "Did not find environment variable"
    db_uri = config.SQLALCHEMY_DATABASE_URI

engine = create_engine(db_uri, echo=True)
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


