import json
import hashlib
import uuid
from models import User
from html_renderer import View
from page_config import get_public_pages, get_page_config
import re

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
        validate_form_result = validate_form(page_name, event['body'])
        if validate_form_result != True:
            return validate_form_result
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
    user = User()
    user_exists = user.find(inputs['username'], True)
    if user_exists != False:
        return get_validation_error_response('username', "Username is already taken.")

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
    else:
        return hashlib.sha256(salted_input).hexdigest()

def authenticate_user(inputs):
    user = User()
    user.find(inputs['username'], True)
    if(user.get('id') == None):
        return get_validation_error_response('username', "Username not found.")
    else:
        user.find(user.get('id'))
        if(user.check_password(inputs['password'])):
            hashed_password = get_hashed_password(inputs['password'])
            session_token = user.get('id') + ':' + hashed_password
            user.set('session_token', session_token)
            user.save()
            return {
                'cookie': 'X-token=' + user.get('session_token'),
                'body':user.get_attributes(),
                'redirect':'home'
            }
        else:
            return get_validation_error_response('password', "Incorrect Password.")

def validate_form(page_name, inputs):
    page_config = get_page_config(page_name)
    is_valid = True
    response =  {
        'body' : {
            'errors': []
        }
    }
    if page_config != None:
        for field, meta in page_config['fields'].items():
            if 'required' in meta and meta['required'] == True:
                validation_response = get_required_validation_response(is_valid,
                                                    field, inputs, meta, response)
                is_valid = validation_response['is_valid']
                response = validation_response['response']
            if 'equals' in meta:
                validation_response = get_equals_validation_response(is_valid,
                                                    field, inputs, meta, response, page_config)
                is_valid = validation_response['is_valid']
                response = validation_response['response']
            if 'type' in meta:
                validation_response = get_type_validation_response(is_valid,
                                                    field, inputs, meta, response)
                is_valid = validation_response['is_valid']
                response = validation_response['response']
    if is_valid == False:
        return response
    return is_valid

def get_required_validation_response(is_valid, field, inputs, meta, response):
    if field not in inputs or inputs[field] == '':
        is_valid = False
        label = meta['label']
        message = "{label} is required.".format(label=label)
        response = get_validation_error_response(field, message, response)
    return {
        'is_valid' : is_valid,
        'response': response
    }

def get_equals_validation_response(is_valid, field, inputs, meta, response, page_config):
    if (field not in inputs or meta['equals'] not in inputs) or inputs[field] != inputs[meta['equals']]:
        is_valid = False
        label = meta['label']
        label2 = page_config['fields'][meta['equals']]['label']
        message = "{label} should be equal to {label2}.".format(label=label, label2=label2)
        response = get_validation_error_response(field, message, response)

    return {
        'is_valid' : is_valid,
        'response': response
    }

def get_type_validation_response(is_valid, field, inputs, meta, response):
    email_pattern = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    if meta['type'] == 'email' and re.match(email_pattern, inputs['email']) == None:
        is_valid = False
        label = meta['label']
        message = "{label} is invalid.".format(label=label)
        response = get_validation_error_response(field, message, response)

    return {
        'is_valid' : is_valid,
        'response': response
    }

def get_validation_error_response(field, message, response=None):
    error = {
        'field' : field,
        'message' : message
    }
    if response != None:
        response['body']['errors'].append(error)
    else:
        response = {
            'body' : {
                'errors': [
                    error
                ]
            }
        }

    return response
