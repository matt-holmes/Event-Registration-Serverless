def get_public_pages():
    return ['sign_in', 'sign_up', 'session_expired']

def get_registration_pages():
    return [
        'register_rsvp',
        'register_activities',
        'register_profile',
        'register_hotel'
    ]

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
                    'label' : 'Email',
                    'type' : 'email'
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
        },
        'register_rsvp' : {
            'fields' : {
                'rsvp' : {
                    'required' : True,
                    'label' : 'Will you be attending?',
                    'type' : 'boolean',
                },
            },
            'layout' : [
                ['rsvp']
            ]
        },
        'register_profile' : {
            'fields' : {
                'first_name' : {
                    'required' : True,
                    'label' : 'First Name',
                    'type' : 'varchar'
                },
                'middle_name' : {
                    'required' : True,
                    'label' : 'Middle Name',
                    'type' : 'varchar'
                },
                'last_name' : {
                    'required' : True,
                    'label' : 'Last Name',
                    'type' : 'varchar'
                },
                'email' : {
                    'required' : True,
                    'label' : 'Email',
                    'type' : 'email'
                },
            },
            'layout' : [
                ['first_name', 'middle_name', 'last_name'],
                ['email']
            ]
        },
        'register_activities' : {
            'fields' : {
                'morning_activity' : {
                    'required' : True,
                    'label' : 'Morning Activity',
                    'type' : 'radio',
                    'values' : ['5K Run', 'Golf', 'Tennis']
                },
                'afternoon_activity' : {
                    'required' : True,
                    'label' : 'Afternoon Activity',
                    'type' : 'radio',
                    'values' : ['Gambling', 'See A Show'],
                },
                'evening_activity' : {
                    'required' : True,
                    'label' : 'Evening Activity',
                    'type' : 'radio',
                    'values' : ['Bar Crawl', 'Gambling', 'See A Show'],
                },
            },
            'layout' : [
                ['morning_activity'],
                ['afternoon_activity'],
                ['evening_activity']
            ]
        },
        'register_hotel' : {
            'fields' : {
                'hotel' : {
                    'required' : True,
                    'label' : '',
                    'type' : 'radio',
                    'values' : ['MGM', 'Aries', 'Bellagio']
                },
                'bed' : {
                    'required' : True,
                    'label' : 'Bed',
                    'type' : 'dropdown',
                    'values' : ['', 'King', 'Doubles']
                },
                'dates_html' : {
                    'type' : 'html',
                    'html' : 'Your checkin date will be 01/01/2019 and check out will be on 01/05/2019'
                }
            },
            'layout' : [
                ['dates_html', 'hotel'],
                ['bed']
            ]
        },
    }

    if page_name in pages_config:
        return pages_config[page_name]

    return None
