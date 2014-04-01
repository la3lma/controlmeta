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


    ##
    ##  Test CRUD for metadata
    ## 
    def test_get_all_meta_of_type(self):
        rv = self.app.get('/media/id/1/metatype/faces')
        self.assertEqual(rv.status_code, 404)

    def test_get_specific_meta_item(self):
        rv = self.app.get('/media/id/1/metaid/1')
        self.assertEqual(rv.status_code, 404)

    def test_post_new_meta(self):
        rv = self.app.post(
            '/media/id/1/metatype/faces',
            headers={'Content-Type': 'text/plain'},
            data='this is amazing')
        self.assertEqual(rv.status_code, 204)                           

    def test_post_new_meta_update(self):
        rv = self.app.post(
            '/media/id/1/meta/metaid/1',
            headers={'Content-Type': 'text/plain'},
            data='this is amazing')
        self.assertEqual(rv.status_code, 404)

    def test_delete_meta(self):
        rv = self.app.delete('/media/id/1/metaid/1')
        self.assertEqual(rv.status_code, 404)
        
    def test_delete_all_meta_of_type(self):
        rv = self.app.delete('/media/id/1/meta/faces')
        self.assertEqual(rv.status_code, 404)

    ##
    ## Task list CRUD
    ##
        
    def test_all_waiting_tasks(self):
        rv = self.app.get('/task/waiting')
        self.assertEqual(rv.status_code, 404)

    def test_next_task_of_type(self):
        rv = self.app.get('/task/waiting/type/face/next')
        self.assertEqual(rv.status_code, 404)

    def test_all_waiting_tasks_of_type(self):
        rv = self.app.get('/task/waiting/type/face')
        self.assertEqual(rv.status_code, 404)

    def test_get_in_progress_list(self):
        rv = self.app.get('/task/type/face/in-progress')
        self.assertEqual(rv.status_code, 404)

    def test_get_done_task_list(self):
        rv = self.app.get('/task/type/face/done')
        self.assertEqual(rv.status_code, 404)

    def test_pick_task_of_type(self):
        rv = self.app.get('/task/waiting/type/face/pick')
        self.assertEqual(rv.status_code, 404)

    def test_declare_task_done(self):
        rv = self.app.post('/task/id/1/done')
        self.assertEqual(rv.status_code, 404)

    def test_create_new_task(self):
        rv = self.app.post(
            '/task/type/face',
            headers={'Content-Type': 'text/plain'},
            data='this is amazing')
        self.assertEqual(rv.status_code, 204)



if __name__ == '__main__':
    unittest.main()

