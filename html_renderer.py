from page_config import get_public_pages, get_registration_pages
import json

class View():
    def make(self, page_name, user=None):
        if(user):
            user_attribites = user.get_attributes()
        else:
            user_attribites = {}

        js_options = self.get_js_options(page_name, user)
        view_parts = self.get_view_parts(page_name)
        page_content_signed = 'page-content-signed-in'
        if page_name in get_public_pages():
            top_nav = ''
            side_nav = ''
            page_content_signed = 'page-content-signed-out'
        else:
            top_nav = view_parts['top_nav.html'].format(
                nav_links=view_parts['nav_links.html'].format(
                    current_step=user.get_current_step(),
                    active_home = self.is_active('active_home', page_name),
                    active_activities = self.is_active('active_activities', page_name),
                    active_register = self.is_active('active_register', page_name)
                ),
                user=user_attribites
            )

            side_nav = view_parts['side_nav.html'].format(
                nav_links=view_parts['nav_links.html'].format(
                    current_step=user.get_current_step(),
                    active_home = self.is_active('active_home', page_name),
                    active_activities = self.is_active('active_activities', page_name),
                    active_register = self.is_active('active_register', page_name)
                )
            )

        header = view_parts['header.html'].format(
            w3_css=view_parts['w3.css'],
            style_css=view_parts['style.css']
        )

        return view_parts['common.html'].format(
            header=header,
            view_content=view_parts[page_name + '.html'],
            footer=view_parts['footer.html'],
            common_js=view_parts['common.js'],
            top_nav=top_nav,
            side_nav=side_nav,
            js_options=js_options,
            page_content_signed=page_content_signed,
            user=user_attribites
        )

    def get_view_parts(self, page_name):
        view_parts = {}
        view_item_names = ['header.html', 'footer.html', 'w3.css', 'style.css',
                            'common.html', 'common.js', 'nav_links.html', 'top_nav.html',
                            'side_nav.html']
        view_item_names.append(page_name + '.html')
        for item in view_item_names:
            with open('views/' + item, encoding='utf8') as file:
                view_parts[item] = file.read()

        return view_parts

    def get_js_options(self, page_name, user):
        js_options = {'page_name':page_name}
        return json.dumps(js_options, ensure_ascii=False)

    def is_active(self, link, page_name):
        if link == 'active_home' and page_name == 'home':
            return 'active'
        if link == 'active_activities' and page_name == 'activities':
            return 'active'
        if link == 'active_register' and page_name in get_registration_pages():
            return 'active'
        return ''
