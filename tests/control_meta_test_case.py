import ctlm
import unittest
import json
import flask.ext.testing
import tempfile
from base64 import b64encode
import ctlm

import engine from database

class Control_meta_test_case(unittest.TestCase):


    # def create_app(self):
    #    app.config.from_object('config.TestConfiguration')
    #    return app


    def setUp(self):
        "Talking to a temporary file database"

        # ctlm.db.create_all()


        self.app = ctlm.app.test_client()



        self.username = "admin"
        self.password = "secret"
        self.auth_headers = {
            'Authorization': 'Basic ' +
            b64encode("{0}:{1}".format(self.username, self.password))
        }

        self.headers = self.auth_headers
        
        json_headers = {'Content-Type': 'application/json'}
        self.json_headers = dict(self.auth_headers.items() + json_headers.items())

        plain_headers = {'Content-Type': 'text/plain'}
        self.plain_headers =  dict(self.auth_headers.items() + plain_headers.items())
        

    
    def tearDown(self):
        "Tear down the tmpfile database"
        pass

