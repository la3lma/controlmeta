#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Test task manipulation

    :copyright: (c) 2014 by Bjørn Remseth
    :license: All rights reserved (at least for now)
"""
import os
import mkeep
import unittest
import json
import flask.ext.testing
from mkeep_test_case import MkeepTestCase

class FullTaskLifecycleTest(MkeepTestCase):

    def test_full_lifecycle_for_single_task(self):

        # Add a task
        rv = self.app.post(
            '/task/type/face',
            headers={'Content-Type': 'text/plain'},
            data='this is amazing')
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

        rv = self.app.get('/task/waiting')
        self.assertEqual(rv.status_code, 404)

        rv = self.app.get('/task/running')
        self.assertEqual(rv.status_code, 200)

        rv = self.app.get('/task/done')
        self.assertEqual(rv.status_code, 404)

        # XXX Then finish the task off and check all the lists
        

if __name__ == '__main__':
     unittest.main()
