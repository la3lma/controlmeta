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
import mkeep
import unittest
import json

from mediametastorage import MediaAndMetaStorage
mms = MediaAndMetaStorage()


class MkeepTestCase(unittest.TestCase):

    def setUp(self):
        "Get a reference to the testclient"
        self.app = mkeep.app.test_client()

    
    def tearDown(self):
        "Nothing to tear down yet"
        pass

    def grok(self):
        pass

    

if __name__ == '__main__':
    unittest.main()

