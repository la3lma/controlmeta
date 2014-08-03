import unittest

from test_empty_crud import SimpleCrudCases
from test_flask_task_manipulations import FullTaskLifecycleTest
from test_media_and_meta_storage_directly import TestMediaAndMetaStorageDirectly
from test_mediametastorage import test_media_meta_storage
from test_task_queue_storage import MkeepTestCase
from test_media_usecases import MediaUsecases
from test_database import DatabaseTestCase
from test_userdb_crud import UserDatabaseTestCases

unit_tests = [SimpleCrudCases,
              FullTaskLifecycleTest,
              TestMediaAndMetaStorageDirectly,
              test_media_meta_storage,
              MkeepTestCase,
              MediaUsecases,
              DatabaseTestCase,
              UserDatabaseTestCases]

def suite(unit_tests):
    new_suite = unittest.TestSuite()
    for s in unit_tests :
        tests = unittest.TestLoader().loadTestsFromTestCase(s)
        new_suite.addTests(tests)
    return new_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite(unit_tests)
    runner.run (test_suite)