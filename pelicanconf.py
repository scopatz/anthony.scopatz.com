#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals


AUTHOR = u'Anthony Scopatz'
SITENAME = u'Anthony Scopatz'
SITEURL = ''

TIMEZONE = 'America/Central'

DEFAULT_LANG = u'en'

THEME = u'octopelican'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# not Blogroll
#LINKS =  (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('numfocus+subscribe@googlegroups.com', 'Join out mailing list'),
          ('https://groups.google.com/forum/#!forum/numfocus', 'Read the archives'),
          )

GITHUB_URL = 'https://github.com/scopatz'
TWITTER_URL = 'https://twitter.com/scopatz'
GOOGLEPLUS_URL = 'https://plus.google.com/u/0/116439624339414215461'

MENUITEMS = [('Projects', 'projects.html'),
             ('Board', 'board.html'),
             ('Membership', 'membership.html'),
             ('Donations', 'donations.html'),
#             ('Sponsors', 'sponsors.html'),
             ('Contact', 'contact.html'),
             ]

DIRECT_TEMPLATES = ('index', 'tags', 'categories', 'archives',)

EXTRA_TEMPLATE_PATHS = ('templates',)
#PAGINATED_DIRECT_TEMPLATES = []
DEFAULT_PAGINATION = 8

# the intended way to add articles to the news feed is to add them to a
# pre-defined category (i.e. it has a directory) or to explicitly give it a
# category
# the default category is "nofeed"
DEFAULT_CATEGORY = 'nofeed'

TYPOGRIFY = True

MARKUP = ('rst', 'md', 'html')

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
#RELATIVE_URLS = False
