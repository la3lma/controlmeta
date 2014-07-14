import ctlm
import unittest
import json
import flask.ext.testing
import tempfile
from base64 import b64encode
import ctlm
from database import init_db
from users.model import UserStorage
class Control_meta_test_case(unittest.TestCase):


    def setUp(self):
        "Talking to a temporary file database"
        init_db()

        # Get the test client
        self.app = ctlm.app.test_client()

        # Set up authentication stuff
        self.username = "admin"
        self.password = "secret"
        self.auth_headers = {
            'Authorization': 'Basic ' +
            b64encode("{0}:{1}".format(self.username, self.password))
        }

        # Convenience headers that combine
        # authentication info and content types.
        self.headers = self.auth_headers
        
        json_headers = {'Content-Type': 'application/json'}
        self.json_headers = dict(self.auth_headers.items() + json_headers.items())

        plain_headers = {'Content-Type': 'text/plain'}
        self.plain_headers =  dict(self.auth_headers.items() + plain_headers.items())
        
        self.base_url = "http://namuu/"
        self.us  = UserStorage(self.base_url)

        email = "control_meta_test_case_dummy_user@bar.baz"
        self.dummy_user = self.us.find_user_by_email(email)
        if not self.dummy_user:
            self.dummy_user = self.us.new_user(email)

    
    def tearDown(self):
        "Tear down the tmpfile database"
        pass


    def get_dummy_user(self):
        return self.dummy_user



