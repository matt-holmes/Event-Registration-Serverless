from page_config import get_public_pages, get_registration_pages, get_page_config
import json
import re

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
            view_content= self.get_view_content(
                view_parts,
                page_name
            ),
            footer=view_parts['footer.html'],
            common_js=view_parts['common.js'],
            top_nav=top_nav,
            side_nav=side_nav,
            js_options=js_options,
            page_content_signed=page_content_signed,
            user=user_attribites
        )

    def get_view_content(self, view_parts, page_name):
        view_html = view_parts[page_name + '.html']
        if page_name in get_registration_pages():
            register_form = self.get_register_form(page_name)
            view_html = view_html.format(
                register_form=register_form
            )

        return view_html

    def get_register_form(self, page_name):
        form_html = '<form class="w3-container w3-card-4 w3-sand">'
        form_html += self.get_progress_bar(page_name)
        page_config = get_page_config(page_name)
        for row in page_config['layout']:
            form_html += '<div class="w3-row row">'
            for field in row:
                form_html += self.field_factory(field, page_config['fields'][field])
            form_html += '</div>'
        form_html += '<p><button type="button" id="submit" class="w3-btn w3-padding w3-dark-grey" style="width:120px">Submit &nbsp; ❯</button></p>'
        form_html += '</form>'
        return form_html

    def get_progress_bar(self, page_name):
        if page_name == 'register_rsvp':
            percent = '0'
        elif page_name == 'register_profile':
            percent = '25'
        elif page_name == 'register_activities':
            percent = '50'
        elif page_name == 'register_hotel':
            percent = '75'
        elif page_name == 'register_complete':
            percent = '100'
        progress_bar = '<div class="w3-round progress-bar">'
        progress_bar += '<div class="w3-container w3-round w3-deep-orange" style="width:{percent}%">{percent}%</div>'
        progress_bar += '</div>'
        return progress_bar.format(percent=percent)

    def field_factory(self, field_name, field_meta):
        if field_meta['type'] == 'boolean':
            return self.get_boolean_field(field_name, field_meta)
        elif field_meta['type'] == 'varchar':
            return self.get_varchar_field(field_name, field_meta)
        elif field_meta['type'] == 'email':
            return self.get_varchar_field(field_name, field_meta)
        elif field_meta['type'] == 'radio':
            return self.get_radio_field(field_name, field_meta)
        elif field_meta['type'] == 'dropdown':
            return self.get_dropdown_field(field_name, field_meta)
        elif field_meta['type'] == 'html':
            return self.get_html_field(field_name, field_meta)
        else:
            return ''

    def get_boolean_field(self, field_name, field_meta):
        values = ['Yes', 'No']
        field_class = self.get_field_class(field_meta, 'radio')
        type = 'radio'
        field_html = ''
        label = '<label class="w3-text-grey">{label_value}</label><br>'
        field_html += label.format(label_value=field_meta['label'])
        for value in values:
            field_html += '<input name="{name}" class="{field_class}" type="{type}" value="{value}"> <label class="w3-text-grey">{label}</label> '
            field_html = field_html.format(name=field_name, field_class=field_class, type=type, value=self.snake_case(value), label=value)
        return field_html

    def get_varchar_field(self, field_name, field_meta):
        field_class = self.get_field_class(field_meta, 'input')
        type = 'input'
        field_html = ''
        label = '<label class="w3-text-grey">{label_value}</label><br>'
        field_html += label.format(label_value=field_meta['label'])
        field_html += '<input name="{name}" class="{field_class}" type="{type}">'
        field_html = field_html.format(name=field_name, field_class=field_class, type=type)
        return field_html

    def get_radio_field(self, field_name, field_meta):
        field_class = self.get_field_class(field_meta, 'radio')
        type = 'radio'
        field_html = ''
        label = '<label class="w3-text-grey">{label_value}</label><br>'
        field_html += label.format(label_value=field_meta['label'])
        for value in field_meta['values']:
            field_html += '<input name="{name}" class="{field_class}" type="{type}" value="{value}"> <label class="w3-text-grey">{label}</label><br> '
            field_html = field_html.format(name=field_name, field_class=field_class, type=type, value=self.snake_case(value), label=value)
        return field_html

    def get_dropdown_field(self, field_name, field_meta):
        type = 'select'
        field_html = ''
        field_html += '<select class="w3-select w3-text-grey" name="{label_value}">'.format(label_value=field_meta['label'])
        for value in field_meta['values']:
            field_html += '<option class="w3-text-grey" value="{value}">{label}</option>'
            field_html = field_html.format(value=self.snake_case(value), label=value)
        field_html += '</select>'
        return field_html

    def get_html_field(self, field_name, field_meta):
        return field_meta['html']

    def get_field_class(self, field_meta, type):
        field_class = 'w3-border w3-' + type
        if field_meta['required'] == True:
            field_class += ' w3-leftbar'
        return field_class

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

    def snake_case(self, string):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string.replace(" ", ""))
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
