from html_renderer import View
from models import User

def build_static_content():
    """
    Builds a set of html files to make testing changes easier.  Otherwise I would
    need to deploy everytime I want to test a small html update

    Returns
    -------
    None

    """
    files = [
        'sign_in',
        'home',
        'sign_up',
        'session_expired',
        'activities',
        'register_rsvp',
        'register_profile',
        'register_activities',
        'register_hotel',
        'register_complete'
    ];

    for file in files:
        with open('static_content/' + file + '.html', 'w+', encoding='utf-8') as newFile:
            view = View()
            user = User()
            user.set('first_name', 'Jon')
            user.set('last_name', 'Doe')
            user.set('rsvp_step_status', None)
            user.set('profile_step_status', None)
            user.set('activities_step_status', None)
            user.set('hotel_step_status', None)
            user.set('status', 'incomplete')
            newFile.write(view.make(file, user))


if __name__ == '__main__':
    build_static_content()
