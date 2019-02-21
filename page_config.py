def get_public_pages():
    return ['sign_in', 'sign_up', 'session_expired']

def get_page_config(page_name):
    pages_config = {
        'sign_in' : {
            'fields' : {
                'username' : {
                    'required' : True,
                    'label' : 'Username'
                },
                'password' : {
                    'required' : True,
                    'label' : 'Password'
                }
            }
        }
    }

    if page_name in pages_config:
        return pages_config[page_name]

    return None
