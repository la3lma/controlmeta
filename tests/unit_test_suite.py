import unittest

from test_empty_crud import SimpleCrudCases

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleCrudCases)
    return suite
    # new_suite = unittest.TestSuite()
    # new_suite.addTest(SimpleCrudCases())
    # return new_suite
    #  s = unittest.TestLoader().loadTestsFromTestCase(SimpleCrudCases())
    # return s

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run (test_suite)