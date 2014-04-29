import application
import unittest
import json
import flask.ext.testing
from mediameta.mediametastorage import MediaAndMetaStorage
from tasks.task_queue_storage import TaskQueueStorage
from base64 import b64encode

class Control_meta_test_case(unittest.TestCase):


    def setUp(self):
        "Get a reference to the testclient"
        
        self.app = application.app.test_client()

        # Injecting dependencies on storage
        application.mms = MediaAndMetaStorage("http://localhost:4711/")
        application.tqs = TaskQueueStorage()

        # XXX This is a kludge.  It seems that the steps above are not
        #     properly clearing existing instances, so this is a workaround.
        application.mms.clear()
        application.tqs.clear()
        
        self.username = "admin"
        self.password = "secret"
        self.auth_headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format(self.username, self.password))
        }

        self.headers = self.auth_headers
        
        json_headers = {'Content-Type': 'application/json'}
        self.json_headers = dict(self.auth_headers.items() + json_headers.items())

        plain_headers = {'Content-Type': 'text/plain'}
        self.plain_headers =  dict(self.auth_headers.items() + plain_headers.items())
        

    
    def tearDown(self):
        "Nothing to tear down yet"
        pass