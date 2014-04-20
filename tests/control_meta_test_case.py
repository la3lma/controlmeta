import application
import unittest
import json
import flask.ext.testing
from mediameta.mediametastorage import MediaAndMetaStorage
from tasks.task_queue_storage import TaskQueueStorage


class Control_meta_test_case(unittest.TestCase):

    def setUp(self):
        "Get a reference to the testclient"
        self.app = application.app.test_client()
        application.mms = MediaAndMetaStorage()
        application.tqs = TaskQueueStorage()

    
    def tearDown(self):
        "Nothing to tear down yet"
        pass
