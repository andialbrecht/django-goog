django-goog -- Another Closure library helper
=============================================

``django-goog`` is an helper app to get kick-started with using the
`Closure library <http://code.google.com/closure/>`_ in a Django
project.

It provides settings and commands to toggle between development and
production mode, but doesn't try to provide on the fly compression or
automatic detection of changes. Deployed code should always be
compiled. Even during development it's much smarter to work with
compiled code (except for JS development itself of course).

``django-goog`` tries to stay out of the way as far as possible.
Therefore it provides simple template tags to load your frontend code
either as is or compiled for a better performance when testing
it. Additionally you can load CSS files distributed with the Closure
library to avoid time consuming CSS work when experimenting with
frontend code. In production mode (i.e. when deployed) ``django-goog``
simply does nothing except rendering a link to your compiled
JavaScript sources.


Installation
------------

To install ``django-goog`` using ``pip`` run

::

   $ pip install -e git+git://github.com/andialbrecht/django-goog.git#egg=django-goog

Then add ``"goog"`` to you ``INSTALLED_APPS`` in your ``settings.py``
and add ``"goog.middleware.GoogDevelopmentMiddleware",`` to
``MIDDLEWARE_CLASSES`` (only needed in development mode to serve
JavaScript dependencies).

TODO: Refer to docs, but write them first.


Homepage: http://github.com/andialbrecht/django-goog
