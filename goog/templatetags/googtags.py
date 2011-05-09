# -*- coding: utf-8 -*-

import os

from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

from goog import utils, views

register = template.Library()


class GoogLinksNode(template.Node):

    def _create_css_link(self, css):
        if not css.endswith('.css'):
            css = '%s.css' % css
        url = reverse('goog_serve_closure', args=('goog/css/%s' % css,))
        return '<link rel="stylesheet" href="%s" />' % url

    def _create_js_tag(self, fname, context):
        tag = '<script src="%s"></script>'
        return template.Template(tag % fname).render(context)

    def _render_dev_mode(self, context):
        html = []
        if 'GOOG_STATIC_URL' not in context:
            context['GOOG_STATIC_URL'] = reverse('goog_serve_closure', args=('',))
        namespaces = getattr(settings, 'GOOG_JS_NAMESPACES', {})
        goog_included = False
        for ns in namespaces:
            data = namespaces[ns]
            if not goog_included and data.get('use_goog', data.get('use_goog_third_party', False)):
                html.insert(0, self._create_js_tag('{{GOOG_STATIC_URL}}goog/base.js', context))
                goog_included = True
            html.append(self._create_js_tag(data['dev_url'], context))
        jsfiles = getattr(settings, 'GOOG_JS_FILES', {})
        for name in jsfiles:
            html.append(self._create_js_tag(jsfiles[name]['url'], context))
        return html

    def _render_compiled(self, context):
        html = []
        jsfiles = getattr(settings, 'GOOG_JS_FILES', {})
        for name in jsfiles:
            urlc = jsfiles[name].get('url_compiled', None)
            if urlc is None:
                urlc = '%s_compiled%s' % os.path.splitext(jsfiles[name]['url'])
            html.append(self._create_js_tag(urlc, context))
        return html

    def render(self, context):
        html = []
        # JS
        dev_mode = getattr(settings, 'GOOG_DEV_MODE', False)
        if dev_mode:
            # CSS
            html.extend(map(self._create_css_link,
                            getattr(settings, 'GOOG_DEV_CSS', [])))
            html.extend(self._render_dev_mode(context))
        else:
            html.extend(self._render_compiled(context))
        return ''.join(html)


@register.tag
def goog_links(parser, token):
    return GoogLinksNode()
