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
import json
import flask.ext.testing
from control_meta_test_case import Control_meta_test_case

class SimpleCrudCases(Control_meta_test_case):

    ## 
    ## Is the front page there?
    ##
    def test_get_root(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)        

    ##
    ## Test CRUD for media
    ##
    def test_get_all_media(self):
        rv = self.app.get('/media', headers=self.headers)
        self.assertEqual(rv.status_code, 200)
        json_data = json.loads(rv.data)
        self.assertEqual(json_data, {})

    def  test_get_specific_media(self):
        rv = self.app.get('/media/id/1', headers=self.headers)
        self.assertEqual(rv.status_code, 404)

    def test_json_post_content_metadata_upload(self):
        rv = self.app.post(
            '/media/',
            headers= self.json_headers,
            data='{"Name": "Test"}' )
        self.assertEqual(rv.status_code, 201)

    # Post to a nonspecified metadata location, get an
    # content ID back

    def test_post_content_metadata_upload(self):
        rv = self.app.post(
            '/media/',
            headers=self.plain_headers,
            data='this is amazing')
        # Check that the return value was OK, created.
        self.assertEqual(rv.status_code, 201)
        # XXX Should  check that there is also an object ID returned.
        #     Can't really find that in the output, and that is a bug.

    def test_delete_item(self):
        rv = self.app.delete('/media/id/1',  headers=self.headers)
        self.assertEqual(rv.status_code, 404)

    ##
    ##  Test CRUD for metadata
    ## 
    def test_get_all_meta_of_type(self):
        rv = self.app.get('/media/id/1/metatype/faces', headers=self.headers)
        self.assertEqual(rv.status_code, 404)


    def test_get_specific_meta_item(self):
        rv = self.app.get('/media/id/1/metaid/1', headers=self.headers)
        self.assertEqual(rv.status_code, 404)


    def test_post_new_meta_to_exististing_document(self):
        # First we create a media entry
        me = self.app.post(
            '/media/',
            headers=self.plain_headers,
            data='this is amazing')
        self.assertEqual(me.status_code, 201)

        returnvalue = json.loads(me.data)
        index = returnvalue['media_id']
        url = '/media/id/'+str(index) + '/metatype/faces'

        rv = self.app.post(
            url,
            headers=self.plain_headers,
            data={"we love": "poker"})
        self.assertEqual(rv.status_code, 200)


    def test_post_new_meta(self):
        rv = self.app.post(
            '/media/metatype/faces',
            headers=self.plain_headers,
            data={"we love": "poker"})
        self.assertEqual(rv.status_code, 201)


    def test_post_new_meta_update(self):
        rv = self.app.post(
            '/media/id/1/meta/metaid/1',
            headers=self.json_headers,
            data={"who would guessed": "this?"})
        self.assertEqual(rv.status_code, 404)

    def test_delete_meta(self):
        rv = self.app.delete('/media/id/1', headers=self.headers)
        self.assertEqual(rv.status_code, 404)
        
    def test_delete_all_meta_of_type(self):
        rv = self.app.delete('/media/id/1/meta/faces', headers=self.headers)
        self.assertEqual(rv.status_code, 404)

    ##
    ## Task list CRUD
    ##
        
    def test_all_waiting_tasks(self):
        rv = self.app.get('/task/waiting', headers = self.headers)
        self.assertEqual(rv.status_code, 200)
        json_data = json.loads(rv.data)
        self.assertEqual(json_data, {})

    def test_all_waiting_tasks_of_type(self):
        rv = self.app.get('/task/waiting/type/face', headers= self.headers)
        self.assertEqual(rv.status_code, 200)
        json_data = json.loads(rv.data)
        self.assertEqual(json_data, {})

    def test_get_in_progress_list(self):
        rv = self.app.get('/task/type/face/running', headers=self.headers)
        self.assertEqual(rv.status_code, 200)
        json_data = json.loads(rv.data)
        self.assertEqual(json_data, {})

    def test_get_done_task_list(self):
        rv = self.app.get('/task/done', headers=self.headers)
        self.assertEqual(rv.status_code, 200)
        json_data = json.loads(rv.data)
        self.assertEqual(json_data, {})

    def test_pick_task_of_type(self):
        rv = self.app.post('/task/waiting/type/face_pick_dummy/pick',
                           headers=self.json_headers,
                           data='{"agentId":"007"}')
        self.assertEqual(rv.status_code, 200)
        json_data = json.loads(rv.data)
        self.assertEqual(json_data, {})


    def test_declare_task_done(self):
        rv = self.app.post(
                '/task/id/9991234/done',
            headers=self.json_headers,
            data='{"agentId":"007"}')
        self.assertEqual(rv.status_code, 404)

    def test_create_task(self):
        rv = self.app.post(
            '/task/type/face',
            headers=self.json_headers,
            data='{"parameter":"value"}')
        self.assertEqual(rv.status_code, 201)


    def test_delete_nonexisting_task(self):
        rv = self.app.delete('/task/id/40400', headers=self.headers)
        self.assertEqual(rv.status_code, 404)

if __name__ == '__main__':
     unittest.main()
