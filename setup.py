#!/usr/bin/env python
#------------------------------------------------------------------------------
# file: $Id: setup.py 346 2012-08-12 17:22:39Z griffin $
# desc: the pxml installation file
# auth: metagriffin <metagriffin@uberdev.org>
# date: 2010/12/21
# copy: (C) CopyLoose 2010 UberDev <hardcore@uberdev.org>, No Rights Reserved.
#------------------------------------------------------------------------------

import sys, os, re, setuptools
from setuptools import setup, find_packages

if sys.hexversion < 0x02070000:
  raise RuntimeError('This package requires python 2.7 or better')

heredir = os.path.abspath(os.path.dirname(__file__))
def read(*parts):
  try:    return open(os.path.join(heredir, *parts)).read()
  except: return ''

test_dependencies = [
  'nose                 >= 1.3.0',
  'coverage             >= 3.6',
  ]

dependencies = [
  'distribute           >= 0.6.24',
  'blessings            >= 1.5',
  ]

entrypoints = {
  'console_scripts': [
    'pxml               = pxml:main',
    ],
  }

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Environment :: Console',
  'Intended Audience :: Developers',
  'Intended Audience :: System Administrators',
  'Natural Language :: English',
  'Operating System :: OS Independent',
  'Programming Language :: Python',
  'Topic :: Software Development',
  'Topic :: Software Development :: Libraries :: Python Modules',
  'Topic :: Utilities',
  'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
  ]

setup(
  name                  = 'pxml',
  version               = '0.2.6',
  description           = 'A python library and command-line tool to "prettify" and colorize XML.',
  long_description      = read('README.rst'),
  classifiers           = classifiers,
  author                = 'metagriffin',
  author_email          = 'mg.pypi@uberdev.org',
  url                   = 'http://github.com/metagriffin/pxml',
  keywords              = 'pretty xml command-line library',
  packages              = find_packages(),
  platforms             = ['any'],
  include_package_data  = True,
  zip_safe              = True,
  install_requires      = dependencies,
  tests_require         = test_dependencies,
  test_suite            = 'pxml',
  entry_points          = entrypoints,
  license               = 'GPLv3+',
)

#------------------------------------------------------------------------------
# end of $Id: setup.py 346 2012-08-12 17:22:39Z griffin $
#------------------------------------------------------------------------------
