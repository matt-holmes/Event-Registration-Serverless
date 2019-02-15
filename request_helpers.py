import json
import hashlib
import uuid
from models import User
from html_renderer import View
from page_config import get_public_pages

def is_signed_in(func):
    def wrapper(page_name, event):
        if page_name in get_public_pages() or is_token_valid(event['headers']):
            return func(page_name, event)
        else:
            if event['method'] == 'GET':
                view = View()
                return view.make('session_expired')
            else:
                return {'redirect' : 'session-expired'}
    return wrapper

@is_signed_in
def handle_request(page_name, event):
    action = event['method']
    if action == 'GET':
        view = View()
        return view.make(page_name)
    elif action == 'POST':
        if page_name == 'sign_up':
            return create_user(event['body'])
        if page_name == 'sign_in':
            return authenticate_user(event['body'])

        return event

def is_token_valid(headers):
    if 'Cookie' not in headers:
        return False
    cookie_parts = headers['Cookie'].split('=')
    if len(cookie_parts) != 2:
        return False
    token_parts = cookie_parts[1].split(':')
    id = token_parts[0]
    token_hashed_password = token_parts[1]
    user = User()
    user.find(id)
    return cookie_parts[1] == user.get('session_token')


def create_user(inputs):
    #TODO validate inputs
    user = User(get_new_user_data(inputs))
    user.save()
    return {
        'cookie': 'X-token=' + user.get('session_token'),
        'body':user.get_attributes(),
        'redirect':'home'
    }

def get_new_user_data(inputs):
    id = str(uuid.uuid4())
    return {
        'id' : id,
        'first_name' : inputs['first_name'],
        'last_name' : inputs['last_name'],
        'email' : inputs['email'],
        'username' : inputs['username'],
        'password' : get_hashed_password(inputs['password'], True),
        'session_token' : id + ':' + get_hashed_password(inputs['password']),
    }

def get_hashed_password(password, for_password = False):
    salt = uuid.uuid4().hex
    salted_input = salt.encode() + password.encode()
    if for_password:
        return hashlib.sha256(salted_input).hexdigest() + ':' + salt
    else: #token
        return hashlib.sha256(salted_input).hexdigest()

def authenticate_user(inputs):
    user = User()
    user.find(inputs['username'], True)
    if(user.get('id') == None):
        return {
            'body' : 'user not found'
        }
    else:
        return {
            'body' : user.get_attributes()
        }
