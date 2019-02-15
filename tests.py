import unittest
from index import *
from request_helpers import *

class TestIndex(unittest.TestCase):

    def test_session_expired_handler(self):
        event = {
            'method' : 'GET',
            'headers' : {}
        }
        context = {}
        result = home_handler(event, context)
        self.assertNotEqual(result.find("session"), -1)

    def test_sign_in_handler(self):
        event = {'method' : 'GET'}
        context = {}
        result = sign_in_handler(event, context)
        self.assertNotEqual(result.find("Sign In"), -1)

    def test_get_new_user_data(self):
        inputs = {
            'first_name' : 'Jon',
            'last_name' : 'Green',
            'email' : 'jgreen@test.com',
            'username' : 'jgreen',
            'password' : 'test1234',
            'confirm_password' : 'test1234'
        }

        result = get_new_user_data(inputs)
        self.assertEqual(result['first_name'], 'Jon')
        self.assertEqual(result['last_name'], 'Green')
        self.assertEqual(result['email'], 'jgreen@test.com')
        self.assertEqual(result['username'], 'jgreen')
        self.assertTrue(result['id'])
        self.assertTrue(result['password'])
        self.assertTrue(result['session_token'])
        with self.assertRaises(KeyError):
            result['confirm_password']




if __name__ == '__main__':
    unittest.main()
