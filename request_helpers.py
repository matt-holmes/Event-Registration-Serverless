import json
import hashlib
import uuid
from models import User
from html_renderer import View
from page_config import get_public_pages, get_page_config, get_registration_pages
import re

def is_signed_in(func):
    """
    Decorator pattern to check if the user is signed in
    ----------
    arg1 : func
        function to be executed if the user is signed in

    Returns
    -------
    Function
        the inner function

    """
    def wrapper(page_name, event):
        user = get_user_from_token(event['headers'])
        event['user'] = user
        if page_name in get_public_pages() or user:
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
    """
    Checks the request type and handles the response
    ----------
    arg1 : page_name
        Page name from the request

    arg1 : event
        Request data
    Returns
    -------
    Mixed
        HTML for Get requests, JSON for posts

    """
    action = event['method']
    if action == 'GET':
        view = View()
        return view.make(page_name, event['user'])
    elif action == 'POST':
        validate_form_result = validate_form(page_name, event['body'])
        if validate_form_result != True:
            return validate_form_result
        elif page_name == 'sign_up':
            return create_user(event['body'])
        elif page_name == 'sign_in':
            return authenticate_user(event['body'])
        elif page_name in get_registration_pages():
            return save_registration_step(event, page_name)

        return event

def get_user_from_token(headers):
    """
    Pulls up the token from a page request cookie to check if the user has a valid session
    ----------
    arg1 : headers
        request headers

    Returns
    -------
    Mixed
        False for invalid cookie, User object for a good session, None for a catch all

    """
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
    if cookie_parts[1] == user.get('session_token'):
        return user
    return None


def create_user(inputs):
    """
    Validates and creates a new user
    ----------
    arg1 : inputs
        inputs from the sign up page

    Returns
    -------
    String
        JSON either validation errors or a cookie and redirect for a success submission

    """
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
    """
    Populates and returns a dict of new user data
    ----------
    arg1 : inputs
        inputs from the sign up page

    Returns
    -------
    Dictionary
        The user data

    """
    id = str(uuid.uuid4())
    return {
        'id' : id,
        'first_name' : inputs['first_name'],
        'last_name' : inputs['last_name'],
        'email' : inputs['email'],
        'username' : inputs['username'],
        'password' : get_hashed_password(inputs['password'], True),
        'session_token' : id + ':' + get_hashed_password(inputs['password']),
        'rsvp_step_status' : None,
        'profile_step_status' : None,
        'activities_step_status' : None,
        'hotel_step_status' : None,
        'status' : 'incomplete'
    }

def get_hashed_password(password, for_password = False):
    """
    Hashes a password for the session and password attribute in the db
    ----------
    arg1 : password
        password to be hashed

    arg2 : for_password
        lets me know if its for the session or the password attr

    Returns
    -------
    String
        Hashed password

    """
    salt = uuid.uuid4().hex
    salted_input = salt.encode() + password.encode()
    if for_password:
        return hashlib.sha256(salted_input).hexdigest() + ':' + salt
    else:
        return hashlib.sha256(salted_input).hexdigest()

def authenticate_user(inputs):
    """
    Autheticates user for the sign-in page
    ----------
    arg1 : inputs
        Inputs from request

    Returns
    -------
    String
        JSON either validation errors or a cookie and redirect for a success submission

    """
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
    """
    Validates a form.
    ----------
    arg1 : page_name
        Page name

    arg2 : inputs
        Inputs from request

    Returns
    -------
    Mixed
        JSON validation errors or True for a success submission

    """
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
    """
    Validates a required field.
    ----------
    arg1 : is_valid
        Boolean to track the form status

    arg2 : field
        Name of field being validated

    arg3 : inputs
        Inputs from request

    arg4 : meta
        Field meta data

    arg5 : response
        JSON response

    Returns
    -------
    String
        JSON of the validation result

    """
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
    """
    Validates that 2 field values are the same (re-enter password).
    ----------
    arg1 : is_valid
        Boolean to track the form status

    arg2 : field
        Name of field being validated

    arg3 : inputs
        Inputs from request

    arg4 : meta
        Field meta data

    arg5 : response
        JSON response

    arg6 : page_config
        Page config

    Returns
    -------
    String
        JSON of the validation result

    """
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
    """
    Validates field type specific (email, phone, etc)
    ----------
    arg1 : is_valid
        Boolean to track the form status

    arg2 : field
        Name of field being validated

    arg3 : inputs
        Inputs from request

    arg4 : meta
        Field meta data

    arg5 : response
        JSON response

    Returns
    -------
    String
        JSON of the validation result

    """
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
    """
    Builds a response of the validation result
    ----------
    arg1 : field
        Name of field being validated

    arg2 : message
        Text to displayed to the user

    arg3 : response
        JSON response

    Returns
    -------
    String
        JSON of the validation result

    """
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

def save_registration_step(event, page_name):
    """
    Updates user on registration page submissions
    ----------
    arg1 : event
        request object

    arg2 : page_name
        Page name

    Returns
    -------
    String
        JSON of the redirect to next step

    """
    user = get_user_from_token(event['headers'])
    user = update_user_step_status(page_name, user)
    for name, value in event['body'].items():
        user.set(name, value)

    user.save()
    return {'redirect' : user.get_current_step()}

def update_user_step_status(page_name, user):
    """
    Updates step status attributes for the page being saved
    ----------
    arg1 : page_name
        Page name

    arg2 : user
        User object

    Returns
    -------
    Object
        User object to be saved
    """
    if page_name == 'register_rsvp':
        user.set('rsvp_step_status', 'complete')
    elif page_name == 'register_profile':
        user.set('profile_step_status', 'complete')
    elif page_name == 'register_activities':
        user.set('activities_step_status', 'complete')
    elif page_name == 'register_hotel':
        user.set('hotel_step_status', 'complete')
        user.set('status', 'complete')

    return user
