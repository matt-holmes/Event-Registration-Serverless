import json
import hashlib
import uuid
from models import User

def home_handler(event, context):
    return handle_request('home', event)

def sign_in_handler(event, context):
    return handle_request('sign_in', event)

def sign_up_handler(event, context):
    return handle_request('sign_up', event)

def session_expired_handler(event, context):
    return handle_request('session_expired', event)

def get_public_pages():
    return ['sign_in', 'sign_up', 'session_expired']

def is_signed_in(func):
    def wrapper(page_name, event):
        if page_name in get_public_pages() or is_token_valid(event['headers']):
            return func(page_name, event)
        else:
            if event['method'] == 'GET':
                return get_view('session_expired')
            else:
                return {'redirect' : 'session-expired'}
    return wrapper

@is_signed_in
def handle_request(page_name, event):
    action = event['method']
    if action == 'GET':
        return get_view(page_name)
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

def get_view(page_name):
    js_options = get_js_options(page_name)
    view_parts = get_view_parts(page_name)
    page_content_signed = 'page-content-signed-in'
    if page_name in get_public_pages():
        view_parts['top_nav.html'] = ''
        view_parts['side_nav.html'] = ''
        page_content_logged_in = ''
        page_content_signed = 'page-content-signed-out'

    header = view_parts['header.html'].format(
        w3_css=view_parts['w3.css'],
        style_css=view_parts['style.css']
    )

    top_nav = view_parts['top_nav.html'].format(
        nav_links=view_parts['nav_links.html']
    )

    side_nav = view_parts['side_nav.html'].format(
        nav_links=view_parts['nav_links.html']
    )

    return view_parts['common.html'].format(
        header=header,
        view_content=view_parts[page_name + '.html'],
        footer=view_parts['footer.html'],
        common_js=view_parts['common.js'],
        top_nav=top_nav,
        side_nav=side_nav,
        js_options=js_options,
        page_content_signed=page_content_signed
    )

def get_view_parts(page_name):
    view_parts = {}
    view_item_names = ['header.html', 'footer.html', 'w3.css', 'style.css',
                        'common.html', 'common.js', 'nav_links.html', 'top_nav.html',
                        'side_nav.html']
    view_item_names.append(page_name + '.html')
    for item in view_item_names:
        with open('views/' + item, encoding='utf8') as file:
            view_parts[item] = file.read()

    return view_parts

def get_js_options(page_name):
    js_options = {'page_name':page_name}
    return json.dumps(js_options, ensure_ascii=False)

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
