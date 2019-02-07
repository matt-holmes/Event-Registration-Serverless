import json
import hashlib
import uuid

def home_handler(event, context):
    return handle_request('home', event)

def sign_in_handler(event, context):
    return handle_request('sign_in', event)

def sign_up_handler(event, context):
    return handle_request('sign_up', event)

def handle_request(page_name, event):
    action = event['method']
    if action == 'GET':
        return get_view(page_name)
    elif action == 'POST':
        if page_name == 'sign_up':
            return create_user(event['body'])

        return event

def get_view(page_name):
    js_options = get_js_options(page_name)
    view_parts = get_view_parts(page_name)

    header = view_parts['header.html'].format(
        w3_css=view_parts['w3.css'],
        style_css=view_parts['style.css']
    )

    return view_parts['common.html'].format(
        header=header,
        view_content=view_parts[page_name + '.html'],
        footer=view_parts['footer.html'],
        common_js=view_parts['common.js'],
        navigation=view_parts['navigation.html'],
        js_options=js_options
    )

def get_view_parts(page_name):
    view_parts = {}
    view_item_names = ['header.html', 'footer.html', 'w3.css', 'style.css',
                        'common.html', 'common.js', 'navigation.html']
    view_item_names.append(page_name + '.html')
    for item in view_item_names:
        with open('views/' + item) as file:
            view_parts[item] = file.read()

    return view_parts

def is_logged_in():
    return False

def get_js_options(page_name):
    js_options = {'page_name':page_name}
    return json.dumps(js_options, ensure_ascii=False)

def create_user(inputs):
    #TODO validate inputs
    user = get_new_user_data(inputs)
    response = get_table_connection('usersTable').put_item(Item=user)
    return {
        'cookie': 'X-token=' + user['session_token'],
        'body':user,
    }

def get_new_user_data(inputs):
    id = str(uuid.uuid4())
    return {
        'id' : id,
        'first_name' : inputs['first_name'],
        'last_name' : inputs['last_name'],
        'email' : inputs['email'],
        'username' : inputs['username'],
        'password' : get_hashed_password(inputs['password'], '1*ys2^#~BD'),
        'session_token' : id + ':' + get_hashed_password(inputs['password']),
    }

def get_hashed_password(password, salt = False):
    if salt == False:
        salt = uuid.uuid4().hex
    salted_input = password.encode('utf-8') + salt.encode('utf-8')
    return hashlib.sha256(salted_input).hexdigest()

def get_table_connection(table_name):
    try:
        boto3
    except NameError:
        import boto3

    dynamodb = boto3.resource('dynamodb',
                region_name='us-east-2',
                endpoint_url="https://dynamodb.us-east-2.amazonaws.com")
    return dynamodb.Table(table_name)
