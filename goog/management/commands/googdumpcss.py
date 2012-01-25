# coding: utf-8

import os

from django.conf import settings
from django.core.management.base import BaseCommand

from goog import utils


class Command(BaseCommand):

    help = 'Print CSS definitions from GOOG_DEV_CSS to stdout.'

    def handle(self, *args, **options):
        for path in getattr(settings, 'GOOG_DEV_CSS', []):
            if not path.endswith('.css'):
                path = '%s.css' % path
            relpath = os.path.join('closure', 'goog', 'css', path)
            path = os.path.join(utils.get_closure_path(), relpath)
            msg = '--- Contents from %s ---' % relpath
            print '/* ' + '-' * len(msg) + ' */'
            print '/* %s */' % msg
            print '/* ' + '-' * len(msg) + ' */'
            print
            with open(path) as r:
                print r.read()
