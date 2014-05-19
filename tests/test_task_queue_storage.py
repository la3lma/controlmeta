#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Test crud against an empty database.  If this doesn't work nothing will.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Tests the Flaskr application.

    :copyright: (c) 2014 by Bjørn Remseth
    :license: All rights reserved (at least for now)
"""
import os
import unittest
import json
from database import init_db

from task.model import RDBQueueStorage
from sqlalchemy import Table, Column, Integer, String, MetaData


class MkeepTestCase(unittest.TestCase):

    def setUp(self):
        "Get a reference to the testclient"
        # Create a new database
        init_db()
        self.tqs = RDBQueueStorage()

    
    def tearDown(self):
        "Nothing to tear down yet"
        pass

    def get_empty_list(self):
        pass

    def test_create_task_with_no_params(self):
        task = self.tqs.create_task("rubberduck", {})
        self.assertTrue(task)
        self.assertEqual("rubberduck", task['taskType'])
        self.assertEqual({}, task['params'])

    def test_create_task_with_params(self):
        params={"apple":"fruit"}
        task = self.tqs.create_task("rubberduck", params)
        self.assertTrue(task)
        self.assertEquals(params,  task['params'])

        
    def test_list_empty_waiting_tasks_list(self):
        tasktype="rubberduck"
        tasklist=self.tqs.list_all_waiting_tasks_of_type(tasktype)

    def test_get_next(self):
        tasktype="snafu"
        runner="sample runner2"
        tasklist=self.tqs.list_all_waiting_tasks_of_type(tasktype)
        self.assertFalse(tasklist)
        task = self.tqs.create_task(tasktype, {})
        tasklist=self.tqs.list_all_waiting_tasks_of_type(tasktype)
        self.assertTrue(tasklist)
        task = self.tqs.pick_next_waiting_task_of_type(tasktype, runner)
        self.assertTrue(task)

    def test_delete_nonexisting_task(self):
        errorDescription = self.tqs.delete_task("1")
        # The error description should be nonempty
        self.assertTrue(errorDescription)
    def test_pick_nonexisting_task(self):
        errorDescription = self.tqs.pick_next_waiting_task_of_type("jalla", "This runner")
        self.assertFalse(errorDescription)

    def test_list_all_nonexisting_done_tasks(self):        
        errorDescription = self.tqs.list_all_done_tasks()
        self.assertFalse(errorDescription)

if __name__ == '__main__':
    unittest.main()

