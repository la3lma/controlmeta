from datetime import datetime


from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import orm
from sqlalchemy import *
from sqlalchemy import schema, types

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = schema.Column(Integer, primary_key=True)
    runner = Column(String)
    tasktype = Column(String)
    params = Column(String)

def create(engine):
        Base.metadata.create_all(engine) 


# def __repr__(self):
#     return "<User(name='%s', fullname='%s', password='%s')>" % (
#         self.name, self.fullname, self.password)
