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
from   persistence.media_meta_proc_persistence import Task
from sqlalchemy import *

class SimpleCrudCases(unittest.TestCase):

    # Set up an ephemeral sqlite-database.
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        self.connection = self.engine.connect()
    
    def tearDown(self):
        "Nothing to tear down yet"
        pass


    ##
    ## Test CRUD for tasks. 
    ## Start by using raw SQL manipulating commands, then co-evolve
    ## the tests into a persistence API that an be used by others tooﬁ
    ##
    def test_store_task(self):
        test_task = Task(
            runner = 'runner 1', 
            tasktype = 'test task',
            params = '{"foo":"bar"}')
        

    def test_delete_task(self):
        pass

    def test_update_task(self):
        pass


if __name__ == '__main__':
     unittest.main()
