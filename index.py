import json
from views import common_html
from views import footer_html
from views import header_html
from views import home_html
from views import sign_in_html
from views import style_css
from views import w3_css

def home_handler(event, context):
    return handle_request(home_html.get_view(), event['method'])

def sign_in_handler(event, context):
    return handle_request(sign_in_html.get_view(), event['method'])

def handle_request(calling_function, action):
    if action == 'GET':
        return get_view(calling_function)

def get_view(page_view):
    header = header_html.get_view().format(w3_css=w3_css.get_view(),
                                            style_css=style_css.get_view())
    footer = footer_html.get_view()
    return common_html.get_view().format(header=header, view_content=page_view,
                                        footer=footer)
