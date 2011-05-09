# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.management.base import BaseCommand

from goog import utils



def _get_infile(data):
    if data['path'] is None:
        url = re.sub('{{[ ]*STATIC_URL[ ]*}}', '', data['url'])
        return finders.find(url)
    return os.path.abspath(data['path'])

def _get_outfile(infile, data):
    parts = os.path.splitext(infile)
    return os.path.abspath('%s_compiled%s' % parts)


class Command(BaseCommand):
    help = 'Compile javascript files.'

    def handle(self, *args, **options):
        closure_path = utils.get_closure_path(interactive=True)
        compiler_jar = utils.get_compiler_jar(interactive=True)
        calcdeps = os.path.join(closure_path, 'closure', 'bin', 'calcdeps.py')
        cmd = [sys.executable, calcdeps,
               '-o', 'compiled',
               '--compiler_jar', compiler_jar,
               '--compiler_flags=--compilation_level=ADVANCED_OPTIMIZATIONS']
        # add namespaces -p path
        goog_included = False
        for key, data in getattr(settings, 'GOOG_JS_NAMESPACES', {}).iteritems():
            if not goog_included and data.get('use_goog', data.get('use_goog_third_party', False)):
                cmd.extend(['-p', closure_path])
                goog_included = True
            cmd.extend(['-p', os.path.abspath(os.path.expanduser(data['path']))])
        # iterate files and compile them
        for key, data in getattr(settings, 'GOOG_JS_FILES', {}).iteritems():
            infile = _get_infile(data)
            outfile = _get_outfile(infile, data)
            this_cmd = cmd+['-i', infile]
            p = subprocess.Popen(this_cmd, stdout=subprocess.PIPE)
            p.wait()
            f = open(outfile, 'w')
            out = p.stdout.read()
            f.write(out)
            f.close()
            print 'Compiled %s (%.3fkB)' % (outfile, len(out)/1024.0)

        # raw_js = []
        # for fname, url_path in utils.get_js_sources():
        #     raw_js.append(open(fname).read())
        # data = [('output_format', 'json'),
        #         ('use_closure_library', 'true'),
        #         ('output_info', 'compiled_code'),
        #         ('compilation_level', 'ADVANCED_OPTIMIZATIONS'),
        #         ('js_code', '\n'.join(raw_js))]
        # data = urllib.urlencode(data)
        # response = urllib2.urlopen('http://closure-compiler.appspot.com/compile',
        #                            data)
        # result = json.loads(response.read())
        # js_config = utils.get_js_config()
        # with open(js_config['compiled_file'], 'w') as f:
        #     f.write(result['compiledCode'])
        # print '%s (%.3fkB)' % (js_config['compiled_file'], (len(result['compiledCode'])/1024.0))
