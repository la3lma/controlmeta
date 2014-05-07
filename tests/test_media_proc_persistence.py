#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Test the SQL based persistence backend.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Tests the Flaskr application.

    :copyright: (c) 2014 by Bjørn Remseth
    :license: All rights reserved (at least for now)
"""
import unittest
from persistence.media_meta_proc_persistence import Task
from persistence.media_meta_proc_persistence import create
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class SimpleCrudCases(unittest.TestCase):

    # Set up an ephemeral sqlite-database.
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        self.connection = self.engine.connect()

        create(self.engine)
        # create a configured "Session" class
        self.Session = sessionmaker(bind=self.engine)

    def tearDown(self):
        "Nothing to tear down yet"
        pass


    def new_session(self):
        self.session = self.Session()

    def commit_session(self):
        self.session.commit()


    def store_new_task(self):
        # First create the task
        self.new_session()
        new_task = Task(
            runner = 'runner 1', 
            tasktype = 'test task',
            params = '{"foo":"bar"}')
        self.session.add(new_task)
        self.commit_session()
        return new_task



    def task_equal(self, t1, t2):
        return  (t1.id == t2.id and
                 t1.runner == t2.runner and
                 t1.tasktype == t2.tasktype and
                 t1.params == t2.params)



    ##
    ## Test CRUD for tasks. 
    ## Start by using raw SQL manipulating commands, then co-evolve
    ## the tests into a persistence API that an be used by others tooﬁ
    ##
    def test_store_then_retrieve_task(self):
        new_task = self.store_new_task()
        # Get the ID of the task.
        id = new_task.id
        
        # Then retrieve the task with that id
        # Kick off a new session
        self.session = self.Session()
        retrieved_task = self.session.query(Task).get(id)

        self.assertTrue(self.task_equal(new_task, retrieved_task))
        

    def test_delete_task(self):
        pass

    def test_update_task(self):
        pass


if __name__ == '__main__':
     unittest.main()
