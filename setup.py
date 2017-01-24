#!/usr/bin/env python

#   This file is part of afaq_scraper, a set of scripts to
#   use different tor guards depending on the network we connect to.
#
#   Copyright (C) 2016 juxor (juxor at riseup dot net)
#
#   afaq_scraper is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License Version 3 of the
#   License, or (at your option) any later version.
#
#   afaq_scraper is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with afaq_scraper.  If not, see <http://www.gnu.org/licenses/>.
#

from setuptools import setup, find_packages
import afaq_scraper
setup(
    name='afaq-scraper',
    version=afaq_scraper.__version__,
    description=afaq_scraper.__description__,
    long_description=afaq_scraper.__long_description__,
    author=afaq_scraper.__author__,
    author_email=afaq_scraper.__author_mail__,
    license='GPLv3+',
    url=afaq_scraper.__website__,

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    dependency_links=[
        "https://pypi.python.org/simple/scrapy",
        "https://pypi.python.org/simple/twisted",
        "https://pypi.python.org/simple/service-identity",
        "https://pypi.python.org/simple/pyyaml",
        "https://pypi.python.org/simple/gitpython",
        "https://pypi.python.org/simple/html2text"
    ],
    extras_require={
        'dev': ['ipython'],
        'test': ['coverage'],
    },

    #entry_points={'scrapy': ['settings = afaq_scraper.settings']},

    scripts=['afaq_scraper/afaq_update.py'],
    keywords='python scrapy afaq anarchism git html markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Environment :: Console",
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 ' +
        'or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
