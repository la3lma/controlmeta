#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Test task manipulation

    :copyright: (c) 2014 by Bjørn Remseth
    :license: All rights reserved (at least for now)
"""
import os
import control_meta_test_case
import unittest
import json
import flask.ext.testing
from control_meta_test_case import Control_meta_test_case



class FullTaskLifecycleTest(Control_meta_test_case):

    def assertReturnedListHasLength(self, url, length):
        rv = self.app.get(url, headers=self.auth_headers)
        self.assertEqual(rv.status_code, 200)
        json_data = json.loads(rv.data)
        self.assertEqual(len(json_data), length)

    def test_full_lifecycle_for_single_task(self):

        # Add a task
        rv = self.app.post(
            '/task/type/face',
            headers=self.json_headers,
            data='{"parameter": "parameter-value"}')
        self.assertEqual(rv.status_code, 201)

        self.assertReturnedListHasLength("task/waiting", 1)
        self.assertReturnedListHasLength("task/running", 0)
        self.assertReturnedListHasLength("task/done",    0)


        # Pick the task up, and start it running
        rv = self.app.post('/task/waiting/type/face/pick',
                           headers=self.json_headers,
                           data='{"agentId":"007"}')
        self.assertEqual(rv.status_code, 200)
        taskdesc = json.loads(rv.data)
        params = taskdesc['params']
        taskid = taskdesc['taskId']

        parameter_value=params['parameter']
        self.assertEquals("parameter-value", parameter_value )

        self.assertReturnedListHasLength("task/waiting", 0)
        self.assertReturnedListHasLength("task/running", 1)
        self.assertReturnedListHasLength("task/done",    0)

        # Then terminate the task
        taskurl =  "/task/id/" + str(taskid)
        doneurl = taskurl +  "/done" 
        rv = self.app.post(
            doneurl,
            data='{"agentId":"007"}',
            headers=self.json_headers)

        foo = self.app.get(taskurl, headers = self.auth_headers)

        self.assertReturnedListHasLength("task/waiting", 0)
        self.assertReturnedListHasLength("task/running", 0)
        self.assertReturnedListHasLength("task/done",    1)


if __name__ == '__main__':
     unittest.main()
