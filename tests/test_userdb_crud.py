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
import flask.ext.testing
from control_meta_test_case import Control_meta_test_case
from users.model import encrypt


class UserDatabaseTestCases(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_encryption(self):
        foo = "xyxxif"
        efoo = encrypt(foo)
        self.assertNotEqual(foo, efoo)

if __name__ == '__main__':
     unittest.main()
