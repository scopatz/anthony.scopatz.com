#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals


AUTHOR = u'Anthony Scopatz'
SITENAME = u'Anthony Scopatz'
SITESUBTITLE = "I think, therefore I amino acid."
SITEURL = 'http://localhost:8000'

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
SOCIAL = (('Other Website', 'http://scopatz.com/'),
          ('Google+', 'https://plus.google.com/u/0/116439624339414215461'),
          ('GitHub', 'https://github.com/scopatz'),
          ('BitBucket', 'https://bitbucket.org/scopatz'),
          ('Twitter', 'https://twitter.com/scopatz'),
          ('LinkedIn', 'http://www.linkedin.com/in/scopatz'),
          )

#DISQUS_SITENAME = ""
GITHUB_URL = 'https://github.com/scopatz'
TWITTER_URL = 'https://twitter.com/scopatz'
GOOGLEPLUS_URL = 'https://plus.google.com/u/0/116439624339414215461'

MENUITEMS = [('Missives', 'category/missives.html'),
             ('Archives', 'archives.html'),
             ('About', 'about.html'),
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
DEFAULT_CATEGORY = 'null'

TYPOGRIFY = True

MARKUP = ('rst', 'md', 'html')

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
#RELATIVE_URLS = False
