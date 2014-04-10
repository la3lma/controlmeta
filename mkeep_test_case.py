import mkeep
import unittest
import json
import flask.ext.testing
from mediametastorage import MediaAndMetaStorage
from task_queue_storage import TaskQueueStorage


class MkeepTestCase(unittest.TestCase):

    def setUp(self):
        "Get a reference to the testclient"
        self.app = mkeep.app.test_client()
        mkeep.mms = MediaAndMetaStorage()
        mkeep.tqs = TaskQueueStorage()

    
    def tearDown(self):
        "Nothing to tear down yet"
        pass
