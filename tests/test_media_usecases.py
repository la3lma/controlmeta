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

from control_meta_test_case import Control_meta_test_case

class MediaUsecases(Control_meta_test_case):

    ##
    ## Create something, then read it, then delete it then fail reading
    ## it.
    ##
    def test_media_and_meta_roundtrip(self):

        # First there should be nothing there
        rv = self.app.get('/media', headers=self.auth_headers)
        self.assertEqual(rv.status_code, 200)
        json_data = json.loads(rv.data)
        self.assertEqual(json_data, {})


        payload="""{
             "Name": "Test",
             "Latitude": 12.59817,
             "Longitude": 52.12873
             }"""

        # Then we upload some mediadata
        rv = self.app.post(
            '/media/',
            headers=self.json_headers,
            data=payload)
        self.assertEqual(rv.status_code, 201)
        rvj = json.loads(rv.data)

        # Pick up the content ID and the content URL
        contentid = rvj.get('media_id')

        # Had we been really concerned with being
        # conformant we would have used this url instead
        # of the paths we use below.
        contenturl = rvj.get('media_url')

        # Now there should be something here
        rv = self.app.get('/media', headers=self.auth_headers)
        self.assertEqual(rv.status_code, 200)

        # Since there is something there, we can get it and 
        # compare it to what we sent in the first place.
        mediaurl = '/media/id/' + str(contentid)
        rv2 = self.app.get(mediaurl, headers=self.auth_headers)
        self.assertEqual(rv2.status_code, 200)
        self.assertEqual(rv2.data, payload)
        
        # Then upload some real content to go with that
        # metadata
        payload2 = 'this is amazing'
        url = '/media/id/' + str(contentid)

        rv3 = self.app.post(
            mediaurl,
            headers=self.plain_headers,
            data=payload2)

        self.assertEqual(rv3.status_code, 201)

        rv4 = self.app.get(mediaurl, headers=self.auth_headers)
        self.assertEqual(rv4.status_code, 200)
        self.assertEqual(rv4.data, payload2)

        # XXX Here we should look up a lot more stuff just to
        # see what we can do roundtripping for.

        from ctlm.views import state
        print "prior to deleting All users = %r"% state.us.find_all_users()
        # Then we nuke everything
        rv = self.app.delete('/media/id/1', headers=self.auth_headers)
        self.assertEqual(rv.status_code, 204)

        print "After deleting All users = %r"% state.us.find_all_users()

        # Finally we check if it's gone
        rv = self.app.get('/media', headers=self.auth_headers)
        self.assertEqual(rv.status_code, 200)
        json_data = json.loads(rv.data)
        self.assertEqual(json_data, {})
    
if __name__ == '__main__':
    unittest.main()

