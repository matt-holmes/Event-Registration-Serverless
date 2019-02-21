import unittest
from index import *
from request_helpers import *
from models import User

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
        self.assertEqual(result['id'], result['session_token'].split(':')[0])
        with self.assertRaises(KeyError):
            result['confirm_password']

    def test_get_and_set_user_attributes(self):
        attributes = {'test_1': 'test'}
        user = User(attributes)
        self.assertEqual('test', user.get('test_1'))
        user.set_attribute('test_1', 'test2')
        self.assertEqual('test2', user.get('test_1'))
        self.assertEqual('test2', user.get_attributes()['test_1'])
        attributes = {'test_1': 'test3'}
        user.set_attributes(attributes)
        self.assertEqual('test3', user.get('test_1'))
        self.assertEqual(None, user.get('test_3'))

    def test_user_check_password(self):
        user = User()
        user.set('password', '1143a939b4b13fd5088b469f0789bfab2194dabf2a0c219fb7bb9b48479d8279:a7072da7e8b042a683732046b01d1208')
        self.assertTrue(user.check_password('test1234'))
        self.assertFalse(user.check_password('test12345'))

    def test_get_hashed_password(self):
        self.assertEqual(1, len(get_hashed_password('test').split(':')))
        self.assertEqual(2, len(get_hashed_password('test', True).split(':')))

    def test_validate_form(self):
        inputs = {
            'username' : 'test',
            'password' : 'password'
        }
        self.assertTrue(validate_form('sign_in', inputs))

        inputs = {
            'username' : '',
        }
        response = validate_form('sign_in', inputs)
        self.assertEqual('username', response['body']['errors'][0]['field'])
        self.assertEqual('Username is required.',
                            response['body']['errors'][0]['message'])
        self.assertEqual('password', response['body']['errors'][1]['field'])
        self.assertEqual('Password is required.',
                            response['body']['errors'][1]['message'])


if __name__ == '__main__':
    unittest.main()
