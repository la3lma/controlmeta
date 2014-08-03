import unittest

from test_empty_crud import SimpleCrudCases
from test_flask_task_manipulations import FullTaskLifecycleTest


unit_tests = [SimpleCrudCases, FullTaskLifecycleTest]

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