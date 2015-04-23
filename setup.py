# -*- coding: utf-8 -*-
"""
    strings2pot
    -----------

    This utility helps you to get localization strings
    from your Apple or Android applications.

    :copyright: (c) 2015 Qurami srl.
    :license: MIT, see LICENSE for more details.
"""

import re
import sys
import codecs
from os import path
from setuptools import setup, find_packages

VERSION = re.search("VERSION = '([^']+)'", codecs.open(
    path.join(path.dirname(__file__), 'strings2pot', '__init__.py'),
    encoding="utf-8",
).read().strip()).group(1)

LONG_DESCRIPTION = open(path.join(path.dirname(__file__), 'README.rst')).read()

REQUIREMENTS = [
]

setup(
    name='strings2pot',
    version=VERSION,
    url='http://qurami.com/',
    license='MIT',
    description='Converts Apple .strings or Android/Java .xml files to POT gettext files.',
    long_description=LONG_DESCRIPTION,
    author='Gianfranco Reppucci',
    author_email='gianfranco.reppucci@qurami.net',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['strings2pot'],
    package_data={},
    zip_safe=False,
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'strings2pot = strings2pot.strings2pot:main',
        ],
    },
)
