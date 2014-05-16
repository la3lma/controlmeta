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
import ctlm
import unittest
import flask.ext.testing
from control_meta_test_case import Control_meta_test_case

class SimpleCrudCases(Control_meta_test_case):

    def setUp(self):
        "Talking to a temporary file database"
        self.app = ctlm.app.test_client()

    def test_get_root(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)        

    def test_newtask(self):
        rv = self.app.get('/newtask/')
        self.assertEqual(rv.status_code, 200)

if __name__ == '__main__':
     unittest.main()
