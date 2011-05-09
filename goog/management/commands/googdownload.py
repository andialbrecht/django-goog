# -*- coding: utf-8 -*-

import os
import shutil
from optparse import make_option

from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand

from goog import utils


class Command(BaseCommand):
    help = "Download Closure library and compiler."
    option_list = BaseCommand.option_list + (
        make_option('--force',
            action='store_true',
            dest='force',
            default=False,
            help='Download files even if they exist locally.'),
        )

    def handle(self, *args, **options):
        force = options.get('force', False)
        download = True
        try:
            lib_path = utils.get_closure_path(interactive=False)
            print 'Closure library found at %s' % lib_path
            if force:
                print 'Removing as requested.'
                shutil.rmtree(lib_path)
            else:
                download = False
        except ImproperlyConfigured:
            pass
        if download:
            utils.get_closure_path(interactive=True)
        download = True
        try:
            jar_path = utils.get_compiler_jar(interactive=False)
            print 'Closure compiler found at %s' % jar_path
            if force:
                print 'Removing as requested.'
                shutil.rmtree(os.path.split(jar_path)[0])
            else:
                download = False
        except ImproperlyConfigured:
            pass
        if download:
            utils.get_compiler_jar(interactive=True)
