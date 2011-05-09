from django.conf import settings
from django.conf.urls.defaults import patterns, include

import goog.urls

class GoogDevelopmentMiddleware(object):

    def devmode_enabled(self, request):
        """Returns True iff the devmode is enabled."""
        if not settings.DEBUG:
            return False
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if x_forwarded_for:
            remote_addr = x_forwarded_for.split(',')[0].strip()
        else:
            remote_addr = request.META.get('REMOTE_ADDR', None)
        if not remote_addr in settings.INTERNAL_IPS:
            return False
        return True

    def process_request(self, request):
        # This urlconf patching is inspired by debug_toolbar.
        # https://github.com/robhudson/django-debug-toolbar
        if self.devmode_enabled(request):
            if request.urlconf != 'goog.urls':
                original_urlconf = getattr(request, 'urlconf', settings.ROOT_URLCONF)
                goog.urls.urlpatterns += patterns(
                    '',
                    ('', include(original_urlconf)),
                )
                request.urlconf = 'goog.urls'
