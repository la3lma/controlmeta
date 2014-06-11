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
from database import init_db, commit_db

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
        
        foo = mms.store_new_meta_from_type("foo", {})
        
        id = foo['ContentId']

        mms.post_media_to_id(id, "text/plain", "foo")

        keys = mms.get_all_media()
        self.assertFalse(not keys)

        mms.delete_media(id)
        rv = mms.delete_media(id)
        commit_db()

        keys = mms.get_all_media()
        self.assertTrue(not keys)


    def test_metadata_roundtrip(self):
        mms=RDBMSMediaAndMetaStorage("http://namuu/")
        retval = mms.create_new_media_entry("text/plain", "jiha")
        doc_id = retval['ContentId']
        
        meta_type = 'bananas'
        payload   = {"amount": "a big bunch"}
        r = mms.store_new_meta_from_id_and_type(doc_id, meta_type, payload)
        meta_id = r['meta_id']
        returned_meta = mms.get_metadata_from_metaid(meta_id)
        self.assertTrue(returned_meta)
        returned_payload = returned_meta['content']
        self.assertEquals(payload, returned_payload)

if __name__ == '__main__':
    unittest.main()

