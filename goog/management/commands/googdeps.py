import os
import subprocess
import sys

from django.conf import settings
from django.core.management.base import BaseCommand

from goog import utils


class Command(BaseCommand):

    def handle(self, *args, **options):
        # TODO(andi): exclude goog namespace. It doesn't make sense to
        # calc dependencies for it.
        closure_path = utils.get_closure_path(interactive=True)
        depswriter = os.path.join(closure_path, 'closure', 'bin', 'build', 'depswriter.py')
        cmd = [sys.executable, depswriter]
        namespaces = getattr(settings, 'GOOG_JS_NAMESPACES', {})
        if not args:
            print 'No namespace given. Available namespaces are %s.' % ', '.join(namespaces)
        for ns in args:
            data = namespaces.get(ns, None)
            if data is None:
                print 'Skipping unknown namespace %r' % ns
            cwd = os.path.abspath(os.path.expanduser(data['path']))
            outfile = os.path.join(cwd, '%s/deps.js' % ns)
            this_cmd = cmd+['--root_with_prefix', '%s/ ../%s' % (ns, ns)]
            if data.get('use_goog', False):
                this_cmd.extend(['--root_with_prefix', '%s ../goog' % (os.path.join(closure_path, 'closure', 'goog'))])
            if data.get('use_goog_third_party', False):
                this_cmd.extend(['--root_with_prefix', '%s ../goog' % (os.path.join(closure_path, 'third_party', 'closure', 'goog'))])
            this_cmd = this_cmd+['--output_file', outfile]
            p = subprocess.Popen(this_cmd, cwd=cwd)
            p.wait()
            if not p.returncode:
                print '%s written.' % outfile
            else:
                print 'ERROR: Failed to genereated deps.js for namespace %s' % ns
