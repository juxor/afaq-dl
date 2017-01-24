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

""""""
import scrapy
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from os import makedirs
from os.path import join, isdir

settings = get_project_settings()


class AfaqSpider(scrapy.Spider):
    name = "afaq"
    allowed_domains = [settings.get('DOMAIN')]
    start_urls = [settings.get('URL')]

    # NOTE: add arguments here to be accepted as command line arguments
    def __init__(self, *args, **kwargs):
        super(AfaqSpider, self).__init__(*args, **kwargs)
        if not isdir(settings.get('HTML_PATH')):
            makedirs(settings.get('HTML_PATH'))
        # if not isdir(settings.get('LOG_PATH')):
        #     makedirs(settings.get('LOG_PATH'))

    def parse(self, response):
        self.logger.debug(response)
        content = response.xpath(settings.get('XPATH_CONTENT')).extract_first()
        page = response.url.split("/")[-1]
        filepath = join(settings.get('HTML_PATH'), page)
        with open(filepath, 'w') as f:
            f.write(content.encode("utf-8"))
        self.logger.info('Saved file %s' % filepath)

        next_page = response.xpath(settings.get('XPATH_NEXT')).extract_first()
        self.logger.debug('Next page %s.', next_page)
        if next_page:
            yield Request(
                response.urljoin(next_page),
                callback=self.parse,
            )
        else:
            self.logger.debug('No next page.')
