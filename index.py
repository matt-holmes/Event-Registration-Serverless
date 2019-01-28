import json

def home_handler(event, context):
    return handle_request('home', event['method'])

def sign_in_handler(event, context):
    return handle_request('sign_in', event['method'])

def handle_request(page_name, action):
    if action == 'GET':
        return get_view(page_name)

def get_view(page_name):
    with open('views/header.html') as file:
        header = file.read()
    with open('views/footer.html') as file:
        footer = file.read()
    with open('views/w3.css') as file:
        w3_css = file.read()
    with open('views/style.css') as file:
        style_css = file.read()
    with open('views/common.html') as file:
        common = file.read()
    with open('views/' + page_name + '.html') as file:
        page_view = file.read()

    header = header.format(w3_css=w3_css, style_css=style_css)
    return common.format(header=header, view_content=page_view, footer=footer)
