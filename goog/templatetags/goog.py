# -*- coding: utf-8 -*-

import os

from django import template
from django.conf import settings

register = template.Library()


CLOSURE_BASE_URL = getattr(
    settings, 'GOOG_CLOSURE_BASE_URL',
    'http://closure-library.googlecode.com/svn/trunk/closure/')


class GoogCssNode(template.Node):

    def __init__(self, css_file):
        self.css_file = css_file

    def render(self, context):
        return ('<link rel="stylesheet" href="%sgoog/css/%s">'
                % (CLOSURE_BASE_URL, self.css_file))


@register.tag
def goog_css(parser, token):
    try:
        tag_name, css_file = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0])
    return GoogCssNode(css_file)


class GoogJsNode(template.Node):

    def _create_js_tag(self, fname, dev_mode, context):
        tag = '<script src="%s"></script>'
        if not dev_mode:
            path, ext = os.path.splitext(fname)
            fname = "%s_compressed%s" % (path, ext)
        return template.Template(tag % fname).render(context)

    def render(self, context):
        dev_mode = getattr(settings, 'GOOG_DEV_MODE', False)
        html = []
        if dev_mode:
            html.append('<script src="%s/goog/base.js"></script>'
                        % CLOSURE_BASE_URL)
        for fname in getattr(settings, 'GOOG_JS_FILES', {}).values():
            html.append(self._create_js_tag(fname, dev_mode, context))
        return ''.join(html)


@register.tag
def goog_js(parser, token):
    return GoogJsNode()
