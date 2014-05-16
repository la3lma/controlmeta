# Too aggressive import list
from sqlalchemy import Integer, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import schema, types
import ctlm

class Task(ctlm.db.Model):
    __tablename__ = 'tasks'
    id = schema.Column(Integer, primary_key=True)
    tasktype = Column(String)

    def __init__(self, tasktype):
        self.tasktype = tasktype

