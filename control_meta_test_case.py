import control_meta
import unittest
import json
import flask.ext.testing
from mediametastorage import MediaAndMetaStorage
from task_queue_storage import TaskQueueStorage


class Control_meta_test_case(unittest.TestCase):

    def setUp(self):
        "Get a reference to the testclient"
        self.app = control_meta.app.test_client()
        control_meta.mms = MediaAndMetaStorage()
        control_meta.tqs = TaskQueueStorage()

    
    def tearDown(self):
        "Nothing to tear down yet"
        pass
