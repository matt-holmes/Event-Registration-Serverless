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
        },
        'sign_up' : {
            'fields' : {
                'first_name' : {
                    'required' : True,
                    'label' : 'First Name'
                },
                'last_name' : {
                    'required' : True,
                    'label' : 'Last Name'
                },
                'email' : {
                    'required' : True,
                    'label' : 'Email'
                },
                'username' : {
                    'required' : True,
                    'label' : 'Username'
                },
                'password' : {
                    'required' : True,
                    'label' : 'Password'
                },
                'confirm_password' : {
                    'required' : True,
                    'equals' : 'password',
                    'label' : 'Confirm Password'
                }
            }
        }
    }

    if page_name in pages_config:
        return pages_config[page_name]

    return None
