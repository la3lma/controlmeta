# Too aggressive import list
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import schema, types
from app.database import Base


class Task(Base):
    __tablename__ = 'tasks'
    id = schema.Column(Integer, primary_key=True)
    tasktype = Column(String)
