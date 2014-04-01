#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    mkeep unit tests
    ~~~~~~~~~~~~~~~~

    Tests the Flaskr application.

    :copyright: (c) 2014 by Bjørn Remseth
    :license: All rights reserved (at least for now)
"""
import os
import mkeep
import unittest

class MkeepTestCase(unittest.TestCase):

    def setUp(self):
        """Get a reference to the testclient"""
        self.app = mkeep.app.test_client()

    
    def tearDown(self):
        """Nothing to tear down yet"""
        pass

    ##
    ## Test CRUD for media
    ##
    def test_get_all_media(self):
        rv = self.app.get('/media')
        # XXX Ensure that the return data is json
        # XXX Ensure that the return data is empty

    def  test_get_specific_media(self):
        rv = self.app.get('/media/id/<id>/media')
        self.assertEqual(rv.status_code, 404)

    def test_post_user_provisioning(self):
        rv = self.app.post(
            '/media/id/1/media',
            headers={'Content-Type': 'text/plain'},
            data='this is amazing')
        self.assertEqual(rv.status_code, 204)

    def test_delete_item(self):
        rv = self.app.delete('/media/id/1')
        self.assertEqual(rv.status_code, 404)


if __name__ == '__main__':
    unittest.main()

