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
from users.model import UserStorage

from mediameta.model import RDBMSMediaAndMetaStorage

class control_meta_test_case(unittest.TestCase):


    def assumeNoKeys(self):
        keys = self.mms.get_all_media()
        self.assertEquals(0, len(keys))

    
    def setUp(self):
        # This should be sufficient
        init_db()
        base_url = "http://namuu/"
        self.mms = RDBMSMediaAndMetaStorage(base_url)
        self.us  = UserStorage(base_url)

        # But this is actually rquired
        self.mms.clean()
        self.assumeNoKeys()
    
    def tearDown(self):
        pass


     # XXX  Repeated between tests, consider moving to common base class
    def get_dummy_user(self):
        # Monkey-patching to create an user, just to satisfy
        # data model constraints.
        email = "foo@bar.baz"
        user = self.us.find_user_by_email(email)
        if not user:
            user = self.us.new_user(email)
        return user


    def test_create_new_media_entry_from_upload(self):
        user = self.get_dummy_user()
        retval = self.mms.create_new_media_entry("text/plain", "jiha", user)
        self.assertTrue(retval)

    def test_create_delete_roundtrip(self):

        user = self.get_dummy_user()
        foo = self.mms.store_new_meta_from_type("foo", {}, user)
        
        id = foo['media_id']

        self.mms.post_media_to_id(id, "text/plain", "foo", user)

        keys = self.mms.get_all_media()
        self.assertFalse(not keys)

        self.mms.delete_media(id, user)
        rv = self.mms.delete_media(id, user)
        commit_db()

        keys = self.mms.get_all_media()
        self.assertTrue(not keys)

     # XXX  Repeated between tests, consider moving to common base class
    def get_dummy_user(self):
        # Monkey-patching to create an user, just to satisfy
        # data model constraints.
        email = "foo@bar.baz"
        user = self.us.find_user_by_email(email)
        if not user:
            user = self.us.new_user(email)
        return user


    def test_metadata_roundtrip(self):
        user = self.get_dummy_user()
        retval = self.mms.create_new_media_entry("text/plain", "jiha", user)
        doc_id = retval['media_id']
        
        meta_type = 'bananas'
        payload   = {"amount": "a big bunch"}
        r = self.mms.store_new_meta_from_id_and_type(doc_id, meta_type, payload, user)
        meta_id = r['meta_id']
        returned_meta = self.mms.get_metadata_from_id(meta_id)
        self.assertTrue(returned_meta)
        returned_payload = returned_meta['meta_content']
        self.assertEquals(payload, returned_payload)



    def inject_metadata(self, meta_content, meta_type, user):
        retval = self.mms.store_new_meta_from_type(meta_type, meta_content, user)
        media_id = retval['media_id']
        meta_id = retval['meta_id']
        return (media_id, meta_id)



    def test_getting_metadata_from_metatype(self):
        meta_content = {"banana" : "apples" }
        meta_type = "eplegreie"
        user = self.get_dummy_user()

        (media_id, meta_id) = self.inject_metadata(meta_content, meta_type, user)
        
        r = self.mms.get_metadata_from_id_and_metatype(media_id, meta_type, user)
        self.assertTrue(r)

        r_content = r[0]['meta_content']

        self.assertEquals(r_content,  meta_content)


    def assert_exists(self, getter, expectation, id):
        exists = True
        id =  str(id)
        try:
            # Will throw exception when something isn't found
            getter(id)

        except ModelException as e:
            exists = False
        self.assertEquals(expectation, exists)

    
    def assert_meta_exists(self, expectation, meta_id):
        self.assert_exists(self.mms.get_metadata_from_id, expectation, meta_id)

    def assert_media_exists(self, expectation, mediaid):
        self.assert_exists(self.mms.get_media, expectation, mediaid)



    def test_cascading_delete_of_meta(self):
        meta_content = {"banana" : "apples" }
        meta_type = "eplegreie"
        user = self.get_dummy_user()
        (media_id, meta_id) = self.inject_metadata(meta_content, meta_type, user)
        
        r = self.mms.get_metadata_from_id_and_metatype(media_id, meta_type, user)
        self.assertTrue(r)
        self.assert_media_exists(True, media_id)
        self.assert_meta_exists(True, meta_id)
        
        l = self.mms.get_all_media()
        r = self.mms.delete_media(media_id, user)
        commit_db()
        l = self.mms.get_all_media()

        # XXX This fails, no deletion happening
        self.assert_meta_exists(False, meta_id)
        self.assert_media_exists(False, media_id) # XXX This fails! The media isn't gone!


if __name__ == '__main__':
    unittest.main()

