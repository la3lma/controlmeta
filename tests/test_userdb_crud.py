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
    

if __name__ == '__main__':
     unittest.main()
