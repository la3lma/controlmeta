from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData

engine = create_engine('sqlite:///:memory:')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
#     metadata = MetaData()
#     players_table = Table('tasks', metadata,
#                           Column('id', Integer, primary_key=True),
#                           Column('status', String),
#                           Column('tasktype', String),
#                           Column('params', String),
#                           Column('runner', String))
    Base.metadata.create_all(bind=engine)