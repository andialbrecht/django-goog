# -*- coding: utf-8 -*-

import logging
import os
import re
import tempfile
import urllib2
import zipfile
from cStringIO import StringIO

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.exceptions import ImproperlyConfigured


# TODO(andi) Make this a setting.
CLOSURE_LIB_URL = 'http://closure-library.googlecode.com/files/closure-library-20110323-r790.zip'
#CLOSURE_LIB_URL = 'http://closure-library.googlecode.com/files/closure-library-20111110-r1376.zip'
#CLOSURE_COMPILER_URL = 'http://closure-compiler.googlecode.com/files/compiler-latest.zip'
CLOSURE_COMPILER_URL = 'http://dl.google.com/closure-compiler/compiler-latest.zip'

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
    path = os.path.abspath(os.path.expanduser(path))
    if not _is_closure_lib_path(path):
        if not interactive:
            msg = 'Could not find Closure library at %s' % path
            log.error(msg)
            raise ImproperlyConfigured(msg)
        else:
            #if os.path.isdir(path) and os.listdir(path):
            #    raise ImproperlyConfigured('Directory %s exists and is not empty' % path)
            answer = raw_input('Download Closure library (Y/n)? ')
            if answer.strip().lower() in ('', 'y', 'yes', 'j'):
                _download_closure_lib(path)
    return path


def get_compiler_jar(interactive=False):
    path = getattr(settings, 'GOOG_COMPILER_JAR', None)
    if path is None:
        path = os.path.join(tempfile.gettempdir(), 'djgoog-compiler', 'compiler.jar')
    path = os.path.abspath(os.path.expanduser(path))
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


def get_js_files(ns):
    """Generator for all JS files in a namespace."""
    ns = getattr(settings, 'GOOG_JS_NAMESPACES', {}).get(ns)
    if not ns or ns.get('path', None) is None:
        raise StopIteration
    for root, dirs, files in os.walk(ns['path']):
        for name in dirs[:]:
            if name.startswith('.') or name == 'CVS':
                dirs.remove(name)
        for name in files:
            if name.startswith('.') or not name.endswith('.js'):
                continue
            yield os.path.join(root, name)


def get_ns_mtime(ns):
    """Returns latest mtime for all JS files in a namespace."""
    latest = None
    for stat in map(os.stat, get_js_files(ns)):
        if latest is None or latest.st_mtime < stat.st_mtime:
            latest = stat
    return latest.st_mtime


def _get_infile(data):
    if data['path'] is None:
        url = re.sub('{{[ ]*STATIC_URL[ ]*}}', '', data['url'])
        return finders.find(url)
    return os.path.abspath(data['path'])

def _get_outfile(infile, data):
    parts = os.path.splitext(infile)
    return os.path.abspath('%s_compiled%s' % parts)



def get_compiled_mtime():
    """Returns earliest compile time."""
    earliest = None
    for js, data in getattr(settings, 'GOOG_JS_FILES', {}).iteritems():
        infile = _get_infile(data)
        outfile = _get_outfile(infile, data)
        stat = os.stat(outfile)
        if earliest is None or earliest.st_mtime > stat.st_mtime:
            earliest = stat
    return earliest.st_mtime


def is_devmode():
    """Returns True iff in development mode."""
    return settings.DEBUG and getattr(settings, 'GOOG_DEV_MODE', False)


def get_abspath(dirpath):
    """Returns absolute path.

    This mainly resolves paths from installed apps in the form
    "app:appname/PATH".
    """
    if dirpath.startswith('app:'):  # resolve app prefix
        appname, dirpath = dirpath[4:].split('/', 1)
        mod = __import__(appname)
        dirpath = os.path.abspath(os.path.join(os.path.dirname(mod.__file__),
                                               dirpath))
    return dirpath


def abspath_for_namespace(info, path):
    """Returns absolute path for a given namespace info."""
    dirpath = info.get('path')
    assert dirpath
    dirpath = get_abspath(dirpath)
    return os.path.abspath(os.path.join(dirpath, '../', path))
