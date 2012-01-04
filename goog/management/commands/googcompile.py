# -*- coding: utf-8 -*-

import os
import subprocess
import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand

from goog import utils


class Command(BaseCommand):
    help = 'Compile javascript files.'

    def handle(self, *args, **options):
        # TODO(andi) Always run googdeps before?
        closure_path = utils.get_closure_path(interactive=True)
        goog_path = os.path.join(closure_path, 'closure', 'goog')
        goog_td_path = os.path.join(closure_path, 'third_party', 'closure', 'goog')
        compiler_jar = utils.get_compiler_jar(interactive=True)
        calcdeps = os.path.join(closure_path, 'closure', 'bin', 'calcdeps.py')
        cmd = [sys.executable, calcdeps,
               '-o', 'compiled',
               '--compiler_jar', compiler_jar,]
        for flag in getattr(settings, 'GOOG_COMPILER_FLAGS',
                            ['--compilation_level=ADVANCED_OPTIMIZATIONS']):
            cmd.append('--compiler_flags=%s' % flag)
        # add namespaces -p path
        goog_included = False
        goog_td_included = False
        for key, data in getattr(settings, 'GOOG_JS_NAMESPACES', {}).iteritems():
            if not goog_included and data.get('use_goog', False):
                cmd.extend(['-p', goog_path])
                goog_included = True
            if not goog_td_included and data.get('use_goog_third_party', False):
                cmd.extend(['-p', goog_td_path])
                goog_td_included = True
            cmd.extend(['-p', os.path.abspath(os.path.expanduser(data['path']))])
        # iterate files and compile them
        for key, data in getattr(settings, 'GOOG_JS_FILES', {}).iteritems():
            infile = utils._get_infile(data)
            if infile is None:
                raise ImproperlyConfigured('Missing JS file: %r' % data)
            outfile = utils._get_outfile(infile, data)
            this_cmd = cmd+['-i', infile]
            p = subprocess.Popen(this_cmd, stdout=subprocess.PIPE)
            stdout, stderr = p.communicate()
            with open(outfile, 'w') as f:
                f.write(stdout)
            print 'Compiled %s (%.3fkB)' % (outfile, len(stdout)/1024.0)

