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

class SimpleCrudCases(unittest.TestCase):

    def setUp(self):
        "Talking to a temporary file database"
        print "ctlm.app=", ctlm.app
        self.app = ctlm.app.test_client()
        print "setUp: self.app", self.app

    def test_get_root(self):
        print "self.app=", self.app
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)        

    def test_newtask(self):
        print "Gazonk"
        rv = self.app.get('/newtask/')
        print "Foo ", rv
        self.assertEqual(rv.status_code, 200)

if __name__ == '__main__':
     unittest.main()
