# -*- coding: utf-8 -*-

import os
import subprocess
import sys

from django.conf import settings
from django.core.management.base import BaseCommand

from goog import utils


class Command(BaseCommand):
    help = 'Compile javascript files.'

    def handle(self, *args, **options):
        # TODO(andi) Always run googdeps before?
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
            infile = utils._get_infile(data)
            outfile = utils._get_outfile(infile, data)
            this_cmd = cmd+['-i', infile]
            p = subprocess.Popen(this_cmd, stdout=subprocess.PIPE)
            p.wait()
            f = open(outfile, 'w')
            out = p.stdout.read()
            f.write(out)
            f.close()
            print 'Compiled %s (%.3fkB)' % (outfile, len(out)/1024.0)

