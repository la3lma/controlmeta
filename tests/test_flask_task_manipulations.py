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

    def test_full_lifecycle_for_single_task(self):

        # Add a task
        rv = self.app.post(
            '/task/type/face',
            headers=self.json_headers,
            data='{"parameter": "parameter-value"}')
        self.assertEqual(rv.status_code, 201)

        rv = self.app.get('/task/waiting', headers=self.auth_headers)
        self.assertEqual(rv.status_code, 200)

        rv = self.app.get('/task/running', headers=self.auth_headers)
        self.assertEqual(rv.status_code, 200)
        json_data = json.loads(rv.data)
        self.assertEqual(json_data, [])

        rv = self.app.get('/task/done', headers=self.auth_headers)
        self.assertEqual(rv.status_code, 200)
        json_data = json.loads(rv.data)
        self.assertEqual(json_data, [])


        # Pick the task up
        rv = self.app.post('/task/waiting/type/face/pick',
                           headers=self.json_headers,
                           data='{"agentId":"007"}')
        self.assertEqual(rv.status_code, 200)
        taskdesc = json.loads(rv.data)
        params = taskdesc['params']
        taskid = taskdesc['taskId']

        parameter_value=params['parameter']
        self.assertEquals("parameter-value", parameter_value )

        # Then terminate the task
        url = "/task/id/" + str(taskid) + "/done" 
        rv = self.app.post(url, headers=self.auth_headers)

    
        rv = self.app.get('/task/waiting', headers=self.json_headers)
        self.assertEqual(rv.status_code, 200)
        json_data = json.loads(rv.data)
        self.assertEqual(json_data, [])

        rv = self.app.get('/task/running', headers=self.json_headers)
        self.assertEqual(rv.status_code, 200)
        json_data = json.loads(rv.data)
        self.assertEqual(json_data, [])

        rv = self.app.get('/task/done', headers=self.json_headers)
        self.assertEqual(rv.status_code, 200)
        json_data = json.loads(rv.data)
        self.assertEqual(len(json_data), 1)


if __name__ == '__main__':
     unittest.main()
