# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab

# Copyright 2016 juxor <ju@riseup.net>

# This file is part of afaq_scraper.
#
# afaq_scraper is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# afaq_scraper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with afaq_scraper.  If not, see <http://www.gnu.org/licenses/>.

# Scrapy settings for afaq_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'afaq_scraper'

SPIDER_MODULES = ['afaq_scraper.spiders']
NEWSPIDER_MODULE = 'afaq_scraper.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'afaq_scraper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'afaq_scraper.middlewares.AfaqScraperSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'afaq_scraper.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'afaq_scraper.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

###############################################################################
import logging
from datetime import datetime
from os.path import dirname, join, abspath

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) \
              Gecko/20100101 Firefox/24.0'
COOKIES_ENABLED = False
HTTPCACHE_ENABLED = True

# custom
URL = 'http://anarchism.pageabode.com/afaq/index.html'
DOMAIN = 'anarchism.pageabode.com'
XPATH_CONTENT = "//div[@class='node']/div"
XPATH_NEXT = '//link[@rel="next"]/@href'
HTML_DIR = 'html'
LOG_DIR = 'log'
DATA_REPO_DIR = 'afaq'
NOW = datetime.utcnow().replace(microsecond=0).isoformat().replace(':', '-')
DEBUG = True

BASE_PATH = dirname(dirname(abspath(__file__)))
ROOT_PATH = dirname(BASE_PATH)
# LOG_FILENAME = NOW + '_' + BOT_NAME + '.log'
# LOG_PATH = join(ROOT_PATH,  LOG_DIR)
# LOG_FULLPATH = join(LOG_PATH,  LOG_FILENAME)
#
# LOG_FILE = LOG_FULLPATH
# LOG_FILENAME = LOG_FILE
LOG_ENABLED = True
# LOG_ENCODING
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOG_FORMAT = '%(asctime)s [%(module)s (settings)] %(levelname)s: %(message)s'
LOG_DATEFORMAT = "%Y-%m-%d %H:%M:%S"
# LOG_STDOUT
# LOG_SHORT_NAMES

DATA_LOCAL_REPO_PATH = join(ROOT_PATH, DATA_REPO_DIR)
HTML_PATH = join(DATA_LOCAL_REPO_PATH, HTML_DIR)

try:
    from settings_local import *
except ImportError:
    pass
