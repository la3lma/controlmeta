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
import application
import unittest
import json

from mediameta.mediametastorage import MediaAndMetaStorage

from control_meta_test_case import Control_meta_test_case

class TestMediaAndMetaStorageDirectly(Control_meta_test_case):

    def setUp(self):
        "Get a reference to the testclient"
        self.app = application.app.test_client()
    
    def tearDown(self):
        "Nothing to tear down yet"
        pass

    def test_create_media_only_delete_roundtrip(self):
        mms = MediaAndMetaStorage("")                
        keys = mms.get_all_meta()
        self.assertTrue(not keys)        
        mms.post_media_to_id("1", "text/plain", "foo")

        keys = mms.get_all_meta()
        self.assertFalse(not keys)

        mms.delete_media(1)
        rv = mms.delete_media('1')
        keys = mms.get_all_meta()
        self.assertTrue(not keys)


    def test_create_meta_then_data(self):
        mms = MediaAndMetaStorage("")
        return_metadata=mms.create_new_media_entry('text/plain', 'foo')
        contentid = return_metadata['ContentId']

        # XXX VERY BOGUS!
        keys = mms.get_all_meta()
        self.assertTrue(keys)        
        mms.post_media_to_id(contentid, "text/plain", "zor")

if __name__ == '__main__':
    unittest.main()

