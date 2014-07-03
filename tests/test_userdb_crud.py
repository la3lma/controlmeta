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


class UserDatabaseTestCases(unittest.TestCase):

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

    def check_verification_url(self, base_url):
        expected_user_url  = "http://localhost/user/1/verification"
        us = UserStorage(base_url)
        url = us.get_user_verification_url(1)
        self.assertEqual(expected_user_url, url)

    def test_verification_url_without_trailing_base_slash(self):
        self.check_verification_url( "http://localhost")

    def test_verification_url_with_trailing_base_slash(self):
        self.check_verification_url( "http://localhost/")
        

if __name__ == '__main__':
     unittest.main()
