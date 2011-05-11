# -*- coding: utf-8 -*-

import os
import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand

from goog import utils


class Command(BaseCommand):
    help = "print out status information about JS files."

    def handle(self, *args, **options):
        # closure lib found?
        downloadinfo = False
        try:
            lib_path = utils.get_closure_path(interactive=False)
            sys.stdout.write('Closure library found at %s\n' % lib_path)
        except ImproperlyConfigured:
            sys.stderr.write(self.style.ERROR('Error: Closure library not found.\n'))
            downloadinfo = True
        # compiler jar found?
        try:
            jar_path = utils.get_compiler_jar(interactive=False)
            sys.stdout.write('Closure compiler found at %s\n' % jar_path)
        except ImproperlyConfigured:
            sys.stderr.write(self.style.ERROR('Error: Closure compiler not found.\n'))
            downloadinfo = True
        if downloadinfo:
            sys.stdout.write('  -> Run "%s googdownload" to download missing dependencies.\n' % sys.argv[0])
        # namespaces up to date?
        namespaces = getattr(settings, 'GOOG_JS_NAMESPACES', {})
        comp_needed = False
        comp_time = utils.get_compiled_mtime()
        if not namespaces :
            sys.stdout.write('No namespaces found.\n')
        else:
            for ns in namespaces:
                if utils.get_ns_mtime(ns) > comp_time:
                    sys.stderr.write(self.style.HTTP_NOT_FOUND('Namespace %s has changes.\n' % ns))
                    comp_needed = True
        # js files up to date?
        for js, data in getattr(settings, 'GOOG_JS_FILES', {}).iteritems():
            infile = utils._get_infile(data)
            if os.stat(infile).st_mtime > comp_time:
                sys.stderr.write(self.style.HTTP_NOT_FOUND('JS file %s has changes.\n' % js))
        if comp_needed:
            sys.stdout.write('  -> Run "%s googcompile" to compile.\n' % sys.argv[0])
        else:
            sys.stdout.write('All compiled files are up-to-date.\n')
        # warning about used CSS files?
        css_files = getattr(settings, 'GOOG_DEV_CSS', [])
        if css_files:
            sys.stderr.write(self.style.HTTP_NOT_FOUND('You\'re using development CSS files: %s.\n' % ', '.join(css_files)))
            sys.stdout.write('  -> Merge them with your static CSS files.\n')
