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
from database import rds_connect_string, get_database_params_from_EBS_envir_params

class DatabaseTestCase(unittest.TestCase):


    def setUp(self):
        self.db_dbname = 'the_database'
        self.db_username = 'the_user'
        self.db_password = 'the_password'
        self.db_hostname = 'the_hostname'
        self.db_port  = '5000'
        self.expected_connect_string = \
            'postgresql://the_user:the_password@the_hostname:5000/the_database'
        self.cfg = {
            'default': {
                'ENGINE': 'postgresql',
                'NAME': self.db_dbname,
                'USER': self.db_username,
                'PASSWORD': self.db_password,
                'HOST': self.db_hostname,
                'PORT': self.db_port
                }
            }


    def test_create_task_with_no_params(self):
        default_cfg = self.cfg['default']

        computed_connect_string = \
            rds_connect_string(default_cfg)

        self.assertEqual(self.expected_connect_string, computed_connect_string)

    def test_get_database_params_from_EBS_envir_params(self):

        environ = {}
        environ['RDS_DB_NAME'] = self.db_dbname
        environ['RDS_USERNAME'] = self.db_username
        environ['RDS_PASSWORD'] = self.db_password
        environ['RDS_HOSTNAME'] = self.db_hostname
        environ['RDS_PORT'] = self.db_port
        
        dbparams = get_database_params_from_EBS_envir_params(environ)
        self.assertEqual(self.cfg, dbparams)


if __name__ == '__main__':
    unittest.main()

