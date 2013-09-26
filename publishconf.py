#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://anthony.scopatz.com'
#RELATIVE_URLS = False
DISQUS_SITENAME = "anthonyscopatz"

FEED_DOMAIN = SITEURL
FEED_RSS = FEED_ALL_RSS = 'feeds/all.rss.xml'
FEED_ATOM = FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

