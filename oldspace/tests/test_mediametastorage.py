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
import app
import unittest
import json

from mediameta.mediametastorage import MediaAndMetaStorage


class control_meta_test_case(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_create_new_media_entry_from_upload(self):
        mms=MediaAndMetaStorage("http://namuu/")
        retval = mms.create_new_media_entry("text/plain", "jiha")
        self.assertTrue(retval)

    def test_create_delete_roundtrip(self):
        mms=MediaAndMetaStorage("http://namuu/")

        keys = mms.get_all_meta()
        self.assertTrue(not keys)        
        mms.post_media_to_id(1, "text/plain", "foo")

        keys = mms.get_all_meta()
        self.assertFalse(not keys)

        mms.delete_media(1)
        rv = mms.delete_media('/media/id/1')
        keys = mms.get_all_meta()
        self.assertTrue(not keys)
        

if __name__ == '__main__':
    unittest.main()

