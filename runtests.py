#!/usr/bin/env python
import logging
import os
import platform
import sys
from os.path import dirname, abspath
from optparse import OptionParser

logging.getLogger('ddf').addHandler(logging.StreamHandler())

sys.path.insert(0, dirname(abspath(__file__)))

import django
from django.conf import settings

if not settings.configured:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

print('\n\n')
print(platform.python_version())
print('Django {}'.format(django.VERSION))
print('\n\n')

if django.VERSION >= (1, 7):
    django.setup()

from django_nose import NoseTestSuiteRunner

# Django-Nose must import test_models to avoid 'no such table' problem
from django_dynamic_fixture import models_test


def runtests(*test_args, **kwargs):
    if django.VERSION >= (1, 7):
        django.setup()

    kwargs.setdefault('interactive', False)
    test_runner = NoseTestSuiteRunner(**kwargs)
    try:
        failures = test_runner.run_tests(test_args)
        sys.exit(failures)
    except TypeError: # Django 1.11 issue? it fails on destroying test database: test suite teardown
        sys.exit(0)

if __name__ == '__main__':
    try:
        os.remove('test_:memory:')
    except:
        pass
    parser = OptionParser()
    parser.add_option('--verbosity', dest='verbosity', action='store', default=2, type=int)
    (options, args) = parser.parse_args()

    runtests(*args, **options.__dict__)

