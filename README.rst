django-goog -- Another Closure library helper
=============================================

``django-goog`` is an helper app to get kick-started with using the
`Closure library <http://code.google.com/closure/>`_ in a Django
project.

It hides all Closure dependency and compilation stuff so that you can
focus on getting your first lines of JS code done. Compare it to
adding a link to JQuery from some CDN when you want to try out some
frontend stuff and want to play with JQuery features.

``django-goog`` tries to stay out of the way as far as possible to let
you switch to `more sophisticated
<http://djangopackages.com/grids/g/asset-managers/>`_ compression
and/or compilation solutions as soon as your frontend code
matures. Therefore it provides simple template tags to load your
frontend code either as is or compiled for a better performance when
testing it. Additionally you can load CSS files distributed with the
Closure library to avoid time consuming CSS work when experimenting
with frontend code.


Installation
------------

To install ``django-goog`` using ``pip`` run

::

   $ pip install -e git+git://github.com/andialbrecht/django-goog.git#egg=django-goog

Then add ``"goog"`` to you ``INSTALLED_APPS`` in your
``settings.py``.


Usage
-----

Since this app focuses on development it leaves it up to the developer
to make sure that there's always an up-to-date compiled version of
the frontend code.

- TODO: describe settings
- TODO: describe compilation


Limitations
-----------

- issues with namespaces in compiled code
- it's no compressor!
