import ctlm
import unittest
import json
import flask.ext.testing
import tempfile
from base64 import b64encode
import ctlm

class Control_meta_test_case(unittest.TestCase):


    # def create_app(self):
    #    app.config.from_object('config.TestConfiguration')
    #    return app


    def setUp(self):
        "Talking to a temporary file database"
        self.app = ctlm.app.test_client()
        # ctlm.db.create_all()
    
    def tearDown(self):
        "Tear down the tmpfile database"
        pass

