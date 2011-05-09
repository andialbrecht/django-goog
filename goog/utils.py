# -*- coding: utf-8 -*-

import logging
import os
import tempfile
import urllib2
import zipfile
from cStringIO import StringIO

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


CLOSURE_LIB_URL = 'http://closure-library.googlecode.com/files/closure-library-20110323-r790.zip'
CLOSURE_COMPILER_URL = 'http://closure-compiler.googlecode.com/files/compiler-latest.zip'

log = logging.getLogger('goog')


def _download_closure_lib(dest):
    print 'Fetching %s' % CLOSURE_LIB_URL,
    response = urllib2.urlopen(CLOSURE_LIB_URL)
    zfile = zipfile.ZipFile(StringIO(response.read()))
    print 'done.'
    print 'Extracting to %s' % dest,
    zfile.extractall(dest)
    print 'done.'


def _download_closure_compiler(dest):
    print 'Fetching %s' % CLOSURE_COMPILER_URL,
    response = urllib2.urlopen(CLOSURE_COMPILER_URL)
    zfile = zipfile.ZipFile(StringIO(response.read()))
    print 'done.'
    print 'Extracting to %s' % dest,
    dirname, _ = os.path.split(dest)
    zfile.extractall(dirname)


def _is_closure_lib_path(path):
    if not os.path.isdir(path):
        return False
    elif not os.path.isdir(os.path.join(path, 'closure', 'goog')):
        return False
    return True


def get_closure_path(interactive=False):
    path = getattr(settings, 'GOOG_CLOSURE_PATH', None)
    if path is None:
        path = os.path.join(tempfile.gettempdir(), 'djgoog-closure-lib')
    if not _is_closure_lib_path(path):
        if not interactive:
            msg = 'Could not find Closure library at %s' % path
            log.error(msg)
            raise ImproperlyConfigured(msg)
        else:
            if os.path.isdir(path) and os.listdir(path):
                raise ImproperlyConfigured('Directory %s exists and is not empty' % path)
            answer = raw_input('Download Closure library (Y/n)? ')
            if answer.strip().lower() in ('', 'y', 'yes', 'j'):
                _download_closure_lib(path)
    return path


def get_compiler_jar(interactive=False):
    path = getattr(settings, 'GOOG_COMPILER_JAR', None)
    if path is None:
        path = os.path.join(tempfile.gettempdir(), 'djgoog-compiler', 'compiler.jar')
    if not os.path.isfile(path):
        if not interactive:
            raise ImproperlyConfigured('Could not find Closure compiuler (%r)' % path)
        else:
            dirname, _ = os.path.split(path)
            if os.path.isdir(dirname) and os.listdir(dirname):
                raise ImproperlyConfigured('Directory %s exists and is not empty' % path)
            answer = raw_input('Download Closure compiler (Y/n)? ')
            if answer.strip().lower() in ('', 'y', 'yes', 'j'):
                _download_closure_compiler(path)
    return path


# def get_js_config():
#     js_config = {'sources': [], 'source_base_url': '/',
#                  'compiled_file': None, 'compiled_url': None}
#     js_config.update(getattr(settings, 'GOOG_JS_FILES', {}))
#     return js_config


# def _collect_js_paths(path):
#     if os.path.splitext(path)[-1] == '.js':
#         yield path
#     elif os.path.isdir(path):
#         for fname in os.listdir(path):
#             if fname.startswith('.'):
#                 continue
#             fname = os.path.join(path, fname)
#             for item in _collect_js_paths(fname):
#                 yield item


# def get_js_sources():
#     js_config = get_js_config()
#     for path in js_config['sources']:
#         for item in reversed(list(_collect_js_paths(path))):
#             url_path = "%s%s" % (js_config['source_base_url'], item[len(path):])
#             yield item, url_path
