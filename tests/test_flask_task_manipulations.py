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
            headers={'Content-Type': 'application/json'},
            data='{"parameter": "parameter-value"}')
        self.assertEqual(rv.status_code, 201)

        rv = self.app.get('/task/waiting')
        self.assertEqual(rv.status_code, 200)

        # XXX in-progress is a stupid name.  Use "running" instead.
        rv = self.app.get('/task/running')
        self.assertEqual(rv.status_code, 404)

        rv = self.app.get('/task/done')
        self.assertEqual(rv.status_code, 404)

        # Pick the task up
        rv = self.app.post('/task/waiting/type/face/pick',
                           headers={'Content-Type': 'application/json'},
                           data='{"agentId":"007"}')
        self.assertEqual(rv.status_code, 200)
        taskdesc=json.loads(rv.data)
        params=taskdesc['params']
        parameter_value=params['parameter']
        self.assertEquals("parameter-value", parameter_value )
    
        

        rv = self.app.get('/task/waiting')
        self.assertEqual(rv.status_code, 404)

        rv = self.app.get('/task/running')
        self.assertEqual(rv.status_code, 200)

        rv = self.app.get('/task/done')
        self.assertEqual(rv.status_code, 404)

        # XXX Then finish the task off and check all the lists
        

if __name__ == '__main__':
     unittest.main()
