# -*- coding: utf-8 -*-

import os

from distutils.core import setup

README = open('README.rst').read()


def find_packages(base):
    yield base.replace('/', '.').replace('\\', '.')
    for path in os.listdir(base):
        new_base = os.path.join(base, path)
        if os.path.isdir(new_base):
            for res in find_packages(new_base):
                yield res


setup(
    name='django-goog',
    version='0.1dev',
    url='https://github.com/andialbrecht/django-goog',
    license='BSD',
    description='Helper application to get started with using the Closure library in Django projects',
    long_description=README,
    author='Andi Albrecht',
    author_email='albrecht.andi@gmail.com',
    packages=list(find_packages('goog')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
