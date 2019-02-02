from index import get_view

def build_static_content():
    files = ['sign_in', 'home', 'sign_up'];

    for file in files:
        with open('static_content/' + file + '.html', 'w+') as newFile:
            newFile.write(get_view(file))


if __name__ == '__main__':
    build_static_content()
