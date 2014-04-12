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
import control_meta
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
        rv = self.app.get('/media')
        self.assertEqual(rv.status_code, 404)

        # Then we upload some mediadata
        rv = self.app.post(
            '/media/',
            headers={'Content-Type': 'application/json'},
            data="""{
             "Name": "Test",
             "Latitude": 12.59817,
             "Longitude": 52.12873
             }""")
        self.assertEqual(rv.status_code, 201)
        rvj=json.loads(rv.data)

        # Pick up the content ID and the content URL
        contentid=rvj.get('ContentId')

        # Had we been really concerned with being
        # conformant we would have used this url instead
        # of the paths we use below.
        contenturl=rvj.get('ContentURL')

        # Now there should be something here
        rv = self.app.get('/media')
        self.assertEqual(rv.status_code, 200)

        # XXX Here we should look at the json and add some more
        #     tests

        # Then upload some real content to go with that
        # content
        rv = self.app.post(
            '/media/id/1', # XXX Should substitute in contentid here
            headers={'Content-Type': 'text/plain'},
            data='this is amazing')
        self.assertEqual(rv.status_code, 201)

        # XXX Here we should look up a lot more stuff just to
        # see what we can do roundtripping for.

        # Then we nuke everything
        rv = self.app.delete('/media/id/1')
        self.assertEqual(rv.status_code, 204)

        # Finally we check if it's gone
        rv = self.app.get('/media')
        self.assertEqual(rv.status_code, 404)
    
if __name__ == '__main__':
    unittest.main()

