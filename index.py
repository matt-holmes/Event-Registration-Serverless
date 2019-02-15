from request_helpers import handle_request

def home_handler(event, context):
    return handle_request('home', event)

def sign_in_handler(event, context):
    return handle_request('sign_in', event)

def sign_up_handler(event, context):
    return handle_request('sign_up', event)

def session_expired_handler(event, context):
    return handle_request('session_expired', event)
    
