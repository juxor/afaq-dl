#!/usr/bin/env python
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
import logging
import os
from utils.convert import convert_dir, html2md
from conf import MD_PATH
from afaq_scraper.settings import LOG_LEVEL, LOG_FORMAT
# LOG_FILENAME,
from afaq_scraper.settings import HTML_PATH

logger = logging.getLogger(__name__)


def main():
    # if not os.path.isdir(os.path.dirname(LOG_FILENAME)):
    #     os.makedirs(os.path.dirname(LOG_FILENAME))
    logging.basicConfig(
                        # filename=LOG_FILENAME,
                        level=LOG_LEVEL,
                        format=LOG_FORMAT)
    convert_dir(HTML_PATH, MD_PATH, html2md, '.md')

if __name__ == '__main__':
    main()
