from request_helpers import handle_request

def home_handler(event, context):
    return handle_request('home', event)

def sign_in_handler(event, context):
    return handle_request('sign_in', event)

def sign_up_handler(event, context):
    return handle_request('sign_up', event)

def session_expired_handler(event, context):
    return handle_request('session_expired', event)

def activities_handler(event, context):
    return handle_request('activities', event)

def register_handler(event, context):
    return handle_request('register', event)

def register_complete_handler(event, context):
    return handle_request('register_complete', event)

def register_rsvp_handler(event, context):
    return handle_request('register_rsvp', event)

def register_profile_handler(event, context):
    return handle_request('register_profile', event)

def register_activities_handler(event, context):
    return handle_request('register_activities', event)

def register_hotel_handler(event, context):
    return handle_request('register_hotel', event)
