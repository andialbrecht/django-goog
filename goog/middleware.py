from django.conf import settings
from django.conf.urls.defaults import patterns, include

import goog.urls
from goog import utils

class GoogDevelopmentMiddleware(object):

    def devmode_enabled(self, request):
        """Returns True iff the devmode is enabled."""
        return utils.is_devmode()

    def process_request(self, request):
        # This urlconf patching is inspired by debug_toolbar.
        # https://github.com/robhudson/django-debug-toolbar
        if self.devmode_enabled(request):
            original_urlconf = getattr(request, 'urlconf', settings.ROOT_URLCONF)
            if original_urlconf != 'goog.urls':
                goog.urls.urlpatterns += patterns(
                    '',
                    ('', include(original_urlconf)),
                )
                request.urlconf = 'goog.urls'
