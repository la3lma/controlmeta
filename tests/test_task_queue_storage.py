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
from database import init_db, commit_db

from task.model import RDBQueueStorage
from sqlalchemy import Table, Column, Integer, String, MetaData
from model_exception import ModelException

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
        self.assertEqual("rubberduck", task['task_type'])
        self.assertEqual({}, task['parameters'])

    def test_create_task_with_params(self):
        params={"apple":"fruit"}
        task = self.tqs.create_task("rubberduck", params)
        self.assertTrue(task)
        self.assertEquals(params,  task['parameters'])

        
    def test_list_empty_waiting_tasks_list(self):
        tasktype="rubberduck"
        tasklist=self.tqs.list_all_waiting_tasks_of_type(tasktype)

    def test_get_next(self):
        tasktype="snafu"
        runner="sample runner2"
        tasklist=self.tqs.list_all_waiting_tasks_of_type(tasktype)
        self.assertFalse(tasklist)
        task = self.tqs.create_task(tasktype, {})
        commit_db()
        tasklist=self.tqs.list_all_waiting_tasks_of_type(tasktype)
        self.assertTrue(tasklist)
        task = self.tqs.pick_next_waiting_task_of_type(tasktype, runner)
        self.assertTrue(task)

    def test_delete_nonexisting_task(self):
        exception_thrown = False
        try:
            self.tqs.delete_task("9999")
        except ModelException as e:
            exeption_thrown = True
        self.assertFalse(exception_thrown)

    def test_delete_existing_task(self):
        tasktype="rubberduckie99"

        # First check that there is no task there
        tasks = self.tqs.list_all_waiting_tasks_of_type(tasktype)
        self.assertFalse(tasks)

        # First create a new task
        params={"apple":"fruitflie"}

        task = self.tqs.create_task(tasktype, params)
        commit_db()
        
        tasks = self.tqs.list_all_waiting_tasks_of_type(tasktype)
        self.assertTrue(tasks)

        task = tasks[0]
        self.assertTrue(task)

        task_id = task['task_id']

        # Then nuke it
        delete_retval = self.tqs.delete_task(task_id)
        self.assertTrue(delete_retval)
        self.assertEquals('deleted', delete_retval['status'])
        commit_db()

        # And check that it's no longer there in a couple of ways
        tasks = self.tqs.list_all_waiting_tasks_of_type(tasktype)
        self.assertFalse(tasks)

        exception_thrown = False
        try:
            self.tqs.check_if_task_exists(task_id)
        except ModelException as e:
            exeption_thrown = True
        self.assertFalse(exception_thrown)
        
    def test_pick_nonexisting_task(self):
        errorDescription = self.tqs.pick_next_waiting_task_of_type("jalla", "This runner")
        self.assertFalse(errorDescription)

    def test_list_all_nonexisting_done_tasks(self):
        errorDescription = self.tqs.list_all_done_tasks()
        self.assertFalse(errorDescription)


    def test_transition_through_lifecycle(self):
        # First create a new task
        params={"apple":"fruitflie"}
        tasktype = "rubberduckie9"
        task = self.tqs.create_task(tasktype, params)
        commit_db()

        self.assertEqual("waiting", task['status'])

        tasks = self.tqs.list_all_waiting_tasks_of_type(tasktype)
        self.assertTrue(tasks)

        task = tasks[0]
        self.assertTrue(task)

        task_id = task['task_id']

        waiting = self.tqs.list_all_waiting_tasks()
        self.assertTrue(waiting)

        result  = self.tqs.declare_as_running(task_id, "gazonk runner")
        self.assertTrue(result)

        task = self.tqs.get_task(task_id)
        self.assertEqual("running", task['status'])
        
        try:
            self.tqs.declare_as_done(task_id, "007")
        except ModelException as e:
            print "Caught model exception " + e.message
            self.assertFalse(True)

        task = self.tqs.get_task(task_id)
        self.assertEqual("done", task['status'])

if __name__ == '__main__':
    unittest.main()

