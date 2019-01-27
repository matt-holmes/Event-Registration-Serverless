import unittest
from index import *

class TestIndex(unittest.TestCase):
    def test_home_handler(self):
        event = {'method' : 'GET'}
        context = {}
        result = home_handler(event, context)
        self.assertNotEqual(result.find("Home"), -1)
    def test_sign_in_handler(self):
        event = {'method' : 'GET'}
        context = {}
        result = sign_in_handler(event, context)
        self.assertNotEqual(result.find("Sign In"), -1)

if __name__ == '__main__':
    unittest.main()
