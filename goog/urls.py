try:
    from django.conf.urls.defaults import patterns, url
except ImportError:  # Django >= 1.6
    from django.conf.urls import patterns, url

urlpatterns = patterns(
    'goog.views',
    url('^__goog__/(?P<path>.*)$', 'serve_closure',
        name='goog_serve_closure'),
    # FIXME(andi): That's a bit ugly to cover third_party as an URL...
    url('^third_party/(?P<path>.*)$', 'serve_closure_thirdparty',
        name='goog_serve_closure_tp'),
)

