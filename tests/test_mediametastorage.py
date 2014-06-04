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
import json
from database import init_db

from mediameta.model import RDBMSMediaAndMetaStorage

class control_meta_test_case(unittest.TestCase):

    def setUp(self):
        init_db()
        pass
    
    def tearDown(self):
        pass

    def test_create_new_media_entry_from_upload(self):
        mms=RDBMSMediaAndMetaStorage("http://namuu/")
        retval = mms.create_new_media_entry("text/plain", "jiha")
        self.assertTrue(retval)

    def test_create_delete_roundtrip(self):
        mms=RDBMSMediaAndMetaStorage("http://namuu/")

        keys = mms.get_all_media()
        self.assertTrue(not keys)        
        mms.post_media_to_id(1, "text/plain", "foo")

        keys = mms.get_all_media()
        self.assertFalse(not keys)

        mms.delete_media(1)
        rv = mms.delete_media('/media/id/1')
        keys = mms.get_all_media()
        self.assertTrue(not keys)


    def test_metadata_roundtrip(self):
        mms=RDBMSMediaAndMetaStorage("http://namuu/")
        mms.post_media_to_id(1, "text/plain", "foo")
        doc_id = 1

        meta_type = 'bananas'
        payload   = {"amount": "a big bunch"}
        meta_id = mms.store_new_meta_from_type(doc_id, meta_type, payload)

        returned_payload = mms.get_metadata_from_id_and_metaid(doc_id, meta_id)
        self.assertEquals(payload, returned_payload)

if __name__ == '__main__':
    unittest.main()

