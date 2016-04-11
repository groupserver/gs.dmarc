# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
import codecs
import os
import sys
from setuptools import setup, find_packages
from version import get_version

name = 'gs.dmarc'
version = get_version()

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.rst"),
                 encoding='utf-8') as f:
    long_description += '\n' + f.read()

requires = ['publicsuffix', ]
if (sys.version_info < (3, 4)):
    requires += ['setuptools', 'enum34']
if (sys.version_info >= (3, )):
    requires += ['dnspython3 >= 1.11.1']
else:
    requires += ['dnspython >= 1.11.1']

setup(name=name,
      version=version,
      description="Look up and report on the DMARC status of a domain.",
      long_description=long_description,
      classifiers=[
          'Development Status :: 4 - Beta',
          "Intended Audience :: Developers",
          'License :: OSI Approved :: Zope Public License',
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='DKIM, SPF, DMARC, email, RFC 7489, RFC 6376, RFC 4408',
      author='Michael JasonSmith',
      author_email='mpj17@onlinegroups.net',
      url='https://github.com/groupserver/{0}'.format(name),
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gs'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      extras_require={'docs': ['Sphinx', ], },
      test_suite="{0}.tests.test_all".format(name),
      tests_require=['mock', ],
      entry_points="""
          # -*- Entry points: -*-
      """,)
