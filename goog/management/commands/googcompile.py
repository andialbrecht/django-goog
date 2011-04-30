# -*- coding: utf-8 -*-

import os
import urllib
import urllib2

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import simplejson as json


class Command(BaseCommand):
    help = 'Compile javascript files.'

    def handle(self, *args, **options):
        for fname in getattr(settings, 'GOOG_JS_FILES', []):
            data = [('output_format', 'json'),
                    ('use_closure_library', 'true'),
                    ('output_info', 'compiled_code'),
                    ('compilation_level', 'ADVANCED_OPTIMIZATIONS')]
            with open(fname) as f:
                raw = f.read()
                data.append(('js_code', raw))
            data = urllib.urlencode(data)
            response = urllib2.urlopen('http://closure-compiler.appspot.com/compile',
                                       data)
            result = json.loads(response.read())
            path, ext = os.path.splitext(fname)
            path += '_compressed'
            fname_out = '%s%s' % (path, ext)
            with open(fname_out, 'w') as f:
                f.write(result['compiledCode'])
            print '%s -> %s (%.3fkB)' % (fname, fname_out, (len(result['compiledCode'])/1024.0))
