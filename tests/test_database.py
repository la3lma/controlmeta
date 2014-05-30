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
import unittest
from database import rds_connect_string

class DatabaseTestCase(unittest.TestCase):


    def test_create_task_with_no_params(self):
        db_name = 'the_database'
        db_username = 'the_user'
        db_password = 'the_password'
        db_hostname = 'the_hostname'
        db_port  = '5000'

        cfg = {
            'default': {
                'ENGINE': 'postgresql',
                'NAME': db_name,
                'USER': db_username,
                'PASSWORD': db_password,
                'HOST': db_hostname,
                'PORT': db_port
                }
            }

        default_cfg = cfg['default']

        expected_connect_string = \
            'postgresql://the_user:the_password@the_hostname:5000/the_database'
        computed_connect_string = \
            rds_connect_string(default_cfg)

        self.assertEqual(expected_connect_string, computed_connect_string)




if __name__ == '__main__':
    unittest.main()

