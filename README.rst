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


Settings
--------

``GOOG_DEV_MODE`` (default: ``False``)
  Set this to ``True`` when developing the JavaScript part of your
  application. If ``False`` the compiled version of your scripts are
  loaded.

``GOOG_CLOSURE_PATH`` (defaults to temp directory)
  Local path to closure libraries. Run ``python manage.py
  googdownload`` to download the Closure library to this directory.

``GOOG_COMPILER_JAR`` (defaults to temp directory)
  Local path to ``compiler.jar``. Run ``python manage.py
  googdownload`` to download the compiler to this path.

``GOOG_JS_NAMESPACES``
  A mapping between namespace names and attributes for each
  namespace. See defnamespaces_ for details.

``GOOG_JS_FILES``
  A mapping between applications scripts and their attributes. See
  defappscripts_ for details.

``GOOG_COMPILER_FLAGS`` (default uses advanced optimizations)
  A list of flags passed to the Closure compiler. The default passes
  '--compilation_level=ADVANCED_OPTIMIZATIONS' to the compiler.

``GOOG_DEV_CSS`` (default: empty)
  A list of short names for default CSS files in development mode. See
  devcss_ for details.


.. _defnamespaces:
Defining Namespaces
-------------------

Each namespace is defined as an entry in ``GOOG_JS_NAMESPACES``
setting. Here's an example entry:

::

  GOOG_JS_NAMESPACES = {
    'ns': {
      'dev_url': '{{STATIC_URL}}jslib/ns/deps.js',
      'path': 'example/static/jslib/ns/',
      'use_goog': True,
      'use_goog_third_party': True,
    }
  }

This entry defines a namespace named 'ns'. ``dev_url`` defines the
(relative) path to the deps.js, that is included in development
mode. ``path`` defines the path to the sources directory. ``use_goog``
and ``use_goog_third_party`` determine whether the Closure libraries
will be included at compile time.


.. _defappscripts:
Defining Application Scripts
----------------------------

Each application script is defined as an entry in ``GOOG_JS_FILES``
setting. Here's an example:

::

  GOOG_JS_FILES = {
    'app': {
      'url': '{{STATIC_URL}}js/app.js',
      'url_compiled': None,
      'path': None
    }
  }

This defines 'app' as an application script with a path pointing to
'url' as the version used for development. 'url_compiled' and 'path'
are calculated by ``django-goog``.


.. _editemplate:
HTML Template
-------------

Add the ``goog_links`` template tag somewhere in the HEAD section of
your HTML base template:

::

  {% load googtags %}
  <html>
    <head>
      {% goog_links %}
    </head>
    <body></body>
  </html>


.. _devcss:
CSS in Development Mode
-----------------------

The UI widgets provided by the Closure library require style sheets
(CSS) to work right. During development it could be a bit annoying to
include (and later exclude) the required CSS files when experimenting
with widgets.

``django-goog`` provides an easy way to serve the default CSS files
that come with Closure library by adding them to the ``GOOG_DEV_CSS``
list in your settings file. The entries are just shortcuts for the
full paths as found in the Closure examples. For example if an example
includes "../../css/button.css" just add "button" to ``GOOG_DEV_CSS``:

::

  GOOG_DEV_CSS = (
    'button', 'dialog', 'linkbutton',
  )

Note that this styles are only served when ``GOOG_DEV_MODE`` is set to
``True`` (and ``DEBUG`` is also set to ``True``). The intention is
that you either merge the Closure libraries' default CSS or add your
own styles to your global CSS file(s).


Commands
--------

The following ``manage.py`` commands are available:

``googdownload``
  Download a suitable Closure library and compiler.

``googdeps NAMESPACE``
  Calculate dependency script (``deps.js``) for the given namespace.

``googcompile``
  Compile all application scripts and namespaces packages.


TODO: Refer to docs, but write them first.


Homepage: http://github.com/andialbrecht/django-goog
