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
from model_exception import ModelException

from mediameta.model import RDBMSMediaAndMetaStorage

class control_meta_test_case(unittest.TestCase):


    def assumeNoKeys(self):
        keys = self.mms.get_all_media()
        self.assertEquals(0, len(keys))

    
    def setUp(self):
        # This should be sufficient
        init_db()

        self.mms=RDBMSMediaAndMetaStorage("http://namuu/")

        # But this is actually rquired
        self.mms.clean()
        self.assumeNoKeys()

    
    def tearDown(self):
        pass

    def test_create_new_media_entry_from_upload(self):
        retval = self.mms.create_new_media_entry("text/plain", "jiha")
        self.assertTrue(retval)

    def test_create_delete_roundtrip(self):
        # Checing that there are no keys available
        
        foo = self.mms.store_new_meta_from_type("foo", {})
        
        id = foo['media_id']

        self.mms.post_media_to_id(id, "text/plain", "foo")

        keys = self.mms.get_all_media()
        self.assertFalse(not keys)

        self.mms.delete_media(id)
        rv = self.mms.delete_media(id)
        commit_db()

        keys = self.mms.get_all_media()
        self.assertTrue(not keys)


    def test_metadata_roundtrip(self):
        retval = self.mms.create_new_media_entry("text/plain", "jiha")
        doc_id = retval['media_id']
        
        meta_type = 'bananas'
        payload   = {"amount": "a big bunch"}
        r = self.mms.store_new_meta_from_id_and_type(doc_id, meta_type, payload)
        meta_id = r['meta_id']
        returned_meta = self.mms.get_metadata_from_metaid(meta_id)
        self.assertTrue(returned_meta)
        returned_payload = returned_meta['meta_content']
        self.assertEquals(payload, returned_payload)



    def inject_metadata(self, meta_content, meta_type):
        retval = self.mms.store_new_meta_from_type(meta_type, meta_content)
        media_id = retval['media_id']
        meta_id = retval['meta_id']
        return (media_id, meta_id)

    def test_getting_metadata_from_metatype(self):
        meta_content = {"banana" : "apples" }
        meta_type = "eplegreie"
        (media_id, meta_id) = self.inject_metadata(meta_content, meta_type)
        
        r = self.mms.get_metadata_from_id_and_metatype(media_id, meta_type)
        self.assertTrue(r)

        r_content = r[0]['meta_content']

        self.assertEquals(r_content,  meta_content)
    
    def assert_meta_exists(self, expectation, metaid):
        exists = True
        try:
            # XXX Make getter names more aligned
            self.mms.get_metadata_from_metaid(metaid)
        except ModelException as e:
            exists = False
        self.assertEquals(expectation, exists)

    def assert_media_exists(self, expectation, mediaid):
        exists = True
        try:
            self.mms.get_media(mediaid)
        except ModelException as e:
            exists = False

        self.assertEquals(expectation, exists)



    def test_cascading_delete_of_meta(self):
        meta_content = {"banana" : "apples" }
        meta_type = "eplegreie"
        (media_id, meta_id) = self.inject_metadata(meta_content, meta_type)
        
        r = self.mms.get_metadata_from_id_and_metatype(media_id, meta_type)
        self.assertTrue(r)
        self.assert_media_exists(True, media_id)
        self.assert_meta_exists(True, meta_id)
        
        r = self.mms.delete_media(media_id)
        commit_db()

        # XXX This fails, no deletion happening
        ## XXX THe presence of "str" here indicates bad design.
        self.assert_meta_exists(False, str(meta_id))
        self.assert_media_exists(False, media_id) # XXX This fails! The media isn't gone!



if __name__ == '__main__':
    unittest.main()

