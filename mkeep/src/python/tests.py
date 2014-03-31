#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    openbtssms unit tests
    ~~~~~~~~~~~~~~~~~~~~~

    Tests the Flaskr application.

    :copyright: (c) 2014 by Bjørn Remseth
    :license: All rights reserved (at least for now)
"""
import os
import openbtssms
import unittest



class OpenBtsSmsTestCase(unittest.TestCase):

    def setUp(self):
        """Get a reference to the testclient"""
        self.app = openbtssms.app.test_client()

    
    def tearDown(self):
        """Nothing to tear down yet"""
        pass

    def test_get_service_configuration(self):
        rv = self.app.get('/service-configuration')
        assert b'mom_instance_id' in rv.data

    def test_post_user_provisioning(self):
        provisioningData = '''{
            "uuid" : "db7cbff5-6258-4282-b1bc-86196d687953",
            "facility" : [ "SMS" ],
            "provision_status" : "ADD"
            }
        '''
        
        rv = self.app.post(
            '/user-provisioning/cafebabe',
            headers={'Content-Type': 'application/json'},
            data=provisioningData)
        self.assertEqual(rv.status_code, 204)

    def test_post_submit_sms(self):
        submitData = '''{
           "sms" : {
                 "recipient" : [ "+4792420683", "+4791119548" ],
                 "originator" : "+4795789351",
                 "text" : "Lorem ipsum"
           },
           "billing" : "SUBSCRIPTION",
           "uuid" : "b4ec63c0-620b-4921-ad14-08afc7f64696",
           "delivery_notification_requested" : false
           }'''
        rv = self.app.post('/submit_sms',
                           headers={'Content-Type': 'application/json'},
                           data=submitData)
        self.assertEqual(rv.status_code, 204)

    def test_get_user_subscription(self):
        rv = self.app.get('/subscription/991')
        self.assertEqual(rv.status_code, 200)

    def test_get_is_subscription_provider(self):
        rv = self.app.get('/subscription/991/is-provider-subscription')
        self.assertEqual(rv.status_code, 200)

if __name__ == '__main__':
    unittest.main()

