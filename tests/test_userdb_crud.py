#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Test the user database

    :copyright: (c) 2014 by Bjørn Remseth
    :license: All rights reserved (at least for now)
"""

import os
import unittest
import json
import flask.ext.testing
from control_meta_test_case import Control_meta_test_case
from  users.model import encrypt
from  users.model import UserVerification
from  users.model import UserEntry
from  users.model import UserStorage
from database import commit_db, db_session


class UserDatabaseTestCases(Control_meta_test_case):

    def test_encryption(self):
        foo = "xyxxif"
        efoo = encrypt(foo)
        self.assertNotEqual(foo, efoo)

    def test_verification_test(self):
        secret = "lkasdjf9jdsaf"
        emvc = UserVerification(secret)
        self.assertTrue(emvc.verify(secret))

    def check_password(self, ue, pw):
        self.assertTrue(ue.check_password(pw))
        self.assertFalse(ue.check_password(pw + "foo"))

    def test_create_user_entry(self):
        pw = "foobarpass"
        ue = UserEntry(pw)
        ue.check_password(pw)

    def test_change_password(self):
        pw = "foobarpass"
        ue = UserEntry(pw)
        pw = "another_password"
        ue.set_password(pw)
        self.assertTrue(ue.check_password(pw))

    def test_api_key_verification(self):
        pw = "foobarpass"
        ue = UserEntry(pw)
        key, secret = ("key xx", "secret xx")
        ue.set_api_keys(key, secret)
        self.assertTrue(ue.check_api_key(secret))
        self.assertFalse(ue.check_api_key(secret + "nonce"))


    def check_user_url(self, base_url):
        expected_user_url  = "http://localhost/user/1"
        us = UserStorage(base_url)
        url = us.get_user_url(1)
        self.assertEqual(expected_user_url, url)

    def test_user_url_with_trailing_base_slash(self):
        self.check_user_url("http://localhost/")

    def test_user_url_without_trailing_base_slash(self):
        self.check_user_url("http://localhost/")

    def test_user_url_without_trailing_base_slash(self):
        base_url = "http://localhost"
        expected_user_url  = "http://localhost/user/1"
        us = UserStorage(base_url)
        url = us.get_user_url(1)
        self.assertEqual(expected_user_url, url)

    def create_user_storage(self):
        base_url = "http://localhost"
        us = UserStorage(base_url)        
        return us

    def check_verification_url(self, base_url):
        expected_user_url  = "http://localhost/user/1/verification"
        us = self.create_user_storage()
        url = us.get_user_verification_url(1)
        self.assertEqual(expected_user_url, url)

    def test_verification_url_without_trailing_base_slash(self):
        self.check_verification_url( "http://localhost")

    def test_verification_url_with_trailing_base_slash(self):
        self.check_verification_url( "http://localhost/")
    
    def new_user_storage(self):
        base_url = "http://localhost"
        us = UserStorage(base_url)
        return us

    def test_new_unused_api_key(self):
        us = self.new_user_storage()
        key = us.new_unused_api_key()
        self.assertTrue(key)

    def create_user(self, email="foo@bar.baz"):
        us = self.create_user_storage()
        user = us.new_user(email)
        return user

    def test_user_unique_email(self):
        email = "foo@bar.baz"
        us = self.create_user_storage()
        user = us.new_user(email)
        exception_detected = False
        try: 
            user2 = us.new_user(email)
        except ModelException as e:
            exception_detected = True
        self.assertFalse(exception_detected)
        

    def test_user_creation(self):
        email = "foo@bar.baz"
        us = self.create_user_storage()
        user = us.new_user(email)
        commit_db()

        all_after_adding = us.find_all_users()
        self.assertTrue(all_after_adding)

        user_id = user.id
        self.assertTrue(user)
        self.assertTrue(user_id)
        self.assertEquals(email, user.email_address)

        # Then check that we can indeed find that user by looking
        # it up through email and id (api_key si something we'll check
        # later)

        user_by_id = us.find_user_by_id(user_id)
        self.assertTrue(user_by_id)
        user_by_email = us.find_user_by_email(email)
        self.assertTrue(user_by_email)
        
        self.assertEquals(user_id, user_by_id.id)
        self.assertEquals(user_id, user_by_email.id)


    # XXX Bad design!!# 
    def assert_user_id_exists(self, us,  userid):
        user = us.find_user_by_id(userid)
        return True and user

    def assert_user_id_does_not_exists(self, us, userid):
        return not self.assert_user_id_exists(us, userid)

    def test_user_deletion(self):
        email = "foo@bar.baz"
        us = self.create_user_storage()
        user = us.new_user(email)
        db_session.add(user)
        commit_db()
        user_id = user.id
        self.assertTrue(user_id)
        self.assert_user_id_exists(us, user_id)
        us.delete_user(user_id)
        self.assert_user_id_does_not_exists(us, user_id)
        
    
    def test_api_keys_roundtrip(self):
        # Create user and assign API keys
        us   = self.create_user_storage()
        email = "foo@bar.bzz"
        user = us.new_user(email)
        commit_db()
        all_after_adding = us.find_all_users()
        self.assertTrue(all_after_adding)
        (api_key, api_secret) = us.new_api_keys(user)
        commit_db()

        
        # Then do a bit of lookup using the API key
        user_found = us.find_user_by_api_key(api_key)
        self.assertTrue(user_found)
        self.assertTrue(user_found.id)
        self.assertEquals(user.id, user_found.id)
        
        # Then change the API keys
        (new_api_key, new_api_secret) = us.new_api_keys(user)
        commit_db()
        
        # Check that we did indeed get  a new key/secret
        self.assertNotEqual(api_key, new_api_key)
        self.assertNotEqual(api_secret, new_api_secret)
        
        # And do the lookup again to see that the new key works
        new_user_found = us.find_user_by_api_key(new_api_key)
        self.assertTrue(new_user_found)
        self.assertEquals(user.id, new_user_found.id)


    def test_api_key_verification(self):
        # Create user and assign API keys
        us   = self.create_user_storage()
        email = "foo@bar.bzz"
        user = us.new_user(email)
        (api_key, api_secret) = us.new_api_keys(user)
        commit_db()

        all_after_adding = us.find_all_users()
        self.assertTrue(all_after_adding)

        # Then test using the api_key/secret to log in
        # as an user

        api_user = us.verify_api_login(api_key, api_secret)
        self.assertTrue(api_user)
        self.assertEquals(user.id, api_user.id)

        # Wrong API key
        api_user = us.verify_api_login(api_key + "lasdf", api_secret)
        self.assertFalse(api_user)

        # Wrong secret
        api_user = us.verify_api_login(api_key, api_secret + "aslfj")
        self.assertFalse(api_user)

        # Wrong secret and API key
        api_user = us.verify_api_login(api_key + "sdf", api_secret + "aslfj")
        self.assertFalse(api_user)

        # Empty API key
        api_user = us.verify_api_login("", api_secret)
        self.assertFalse(api_user)

        # Empty API key
        api_user = us.verify_api_login(api_key, "")
        self.assertFalse(api_user)


    def disabled_test_login_verification(self):
        # Create user and assign API keys
        us   = self.create_user_storage()
        email = "foo@bar.bzz"
        password = "deepsecret"
        user = us.new_user(email)
        user.set_password(password)
        commit_db()
        all_after_adding = us.find_all_users()
        self.assertTrue(all_after_adding)

        # Then test using the api_key/secret to log in
        # as an user
        login_user = us.verify_user_login(email, password)
        self.assertTrue(login_user)
        self.assertEquals(user.id, login_user.id)


        # Wrong username
        login_user = us.verify_user_login(email + "lkadfshj", password)
        self.assertFalse(login_user)

        # Wrong password
        login_user = us.verify_user_login(email, password + "lkadfshj")
        self.assertFalse(login_user)

        # empty username
        login_user = us.verify_user_login("", password)
        self.assertFalse(login_user)

        # empty username
        login_user = us.verify_user_login(email, "")
        self.assertFalse(login_user)


if __name__ == '__main__':
     unittest.main()
