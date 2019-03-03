from html_renderer import View
from models import User

def build_static_content():
    files = ['sign_in', 'home', 'sign_up', 'session_expired'];

    for file in files:
        with open('static_content/' + file + '.html', 'w+', encoding='utf-8') as newFile:
            view = View()
            user = User()
            user.set('first_name', 'Jon')
            user.set('last_name', 'Doe')
            newFile.write(view.make(file, user))


if __name__ == '__main__':
    build_static_content()
