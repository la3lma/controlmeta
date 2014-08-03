import ctlm
import unittest
import json
import flask.ext.testing
import tempfile
from base64 import b64encode
import ctlm
from database import init_db, commit_db
from users.model import UserStorage
from ctlm.views import state

class Control_meta_test_case(unittest.TestCase):

    def setUp(self):
        "Talking to a temporary file database"
        init_db()

        # Get the test client
        self.app = ctlm.app.test_client()

        # Inject test user
        self.base_url = "http://namuu/"
        # XXX This is highly bogus.!
        self.us  = UserStorage(self.base_url)

        email = "control_meta_test_case_dummy_user@bar.baz"
        self.username = email
        self.password = "secret"
        state.us.new_user_with_password(self.username, self.password)
        commit_db()

        self.dummy_user = self.us.find_user_by_email(email)
        self.assertTrue(self.dummy_user)

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
        
    
    def tearDown(self):
        self.us.clean()
        state.clean()



    def get_dummy_user(self):
        return self.dummy_user
