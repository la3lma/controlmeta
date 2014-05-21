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
        errorDescription = self.tqs.delete_task("9999")
        print "errorDescription = ", errorDescription
        # The error description should be nonempty
        self.assertTrue(errorDescription)

    def test_delete_existing_task(self):

        # First create a new task
        params={"apple":"fruitflie"}
        task = self.tqs.create_task("rubberduckie", params)
        print "task = " , task

        task_id = task['taskId']

        # Then check that it's there
        # (the check is for falsehood since check_if_task_exists
        # XXX perversely returns empty (interpreted as "no error" 
        # if it's there)
        self.assertFalse(self.tqs.check_if_task_exists(task_id))

        # Then nuke it
        errorDescription = self.tqs.delete_task(task_id)

        # And check that it's no longer there
        self.assertTrue(errorDescription)

        
    def test_pick_nonexisting_task(self):
        errorDescription = self.tqs.pick_next_waiting_task_of_type("jalla", "This runner")
        self.assertFalse(errorDescription)

    def test_list_all_nonexisting_done_tasks(self):        
        errorDescription = self.tqs.list_all_done_tasks()
        self.assertFalse(errorDescription)

    def test_transition_through_lifecycle(self):
        # First create a new task
        params={"apple":"fruitflie"}
        task = self.tqs.create_task("rubberduckie9", params)

        self.assertEqual("waiting", task['status'])
        task_id = task['taskId']

        result  = self.tqs.declare_as_running(task_id, "gazonk runner")
        self.assertFalse(result)

        task = self.tqs.get_task(task_id)
        self.assertEqual("running", task['status'])

        result  = self.tqs.declare_as_done(task_id)
        self.assertFalse(result)

        task = self.tqs.get_task(task_id)
        self.assertEqual("done", task['status'])

if __name__ == '__main__':
    unittest.main()

