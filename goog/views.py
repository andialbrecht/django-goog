import mimetypes
import os

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotModified
from django.utils.http import http_date, parse_http_date

from goog import utils


def _guess_mimetype(path, default_type='application/octet-stream'):
    """Shortcut for mimetypes.guess_type."""
    return mimetypes.guess_type(path)[0] or default_type


def serve_closure(request, path):
    ns = path.split('/')[0]
    if ns == 'goog':
        return _serve_closure(request, path,
                              ('closure/', 'third_party/closure/'))
    else:
        namespaces = getattr(settings, 'GOOG_JS_NAMESPACES', {})
        if ns in namespaces and namespaces[ns].get('path'):
            full_path = utils.abspath_for_namespace(namespaces[ns], path)
        else:
            full_path = path  # simply try to serve the file directly
        try:
            stat = os.stat(full_path)
        except OSError:
            return HttpResponseNotFound(path)
        return _serve_file(request, stat, path, full_path)


def _serve_closure(request, path, prefixes):
    closure_path = utils.get_closure_path()
    full_path = None
    stat = None
    for prefix in prefixes:
        full_path = os.path.join(closure_path, prefix, path)
        try:
            stat = os.stat(full_path)
            break
        except OSError:
            pass
    if full_path is None or stat is None:
        return HttpResponseNotFound(path)
    return _serve_file(request, stat, path, full_path)

def _serve_file(request, stat, rel_path, full_path):
    since = request.META.get('HTTP_IF_MODIFIED_SINCE')
    mimetype = _guess_mimetype(rel_path)
    if since and parse_http_date(since) > stat.st_mtime:
        return HttpResponseNotModified(mimetype=mimetype)
    response = HttpResponse(open(full_path, 'rb').read(), mimetype=mimetype)
    response["Last-Modified"] = http_date(stat.st_mtime)
    return response


def serve_closure_thirdparty(request, path):
    return _serve_closure(request, os.path.join('third_party/', path))
