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
import subprocess
import codecs
import html2text
from os import listdir, makedirs
from os.path import join, splitext, isdir
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def html2md(text):
    logger.info('Converting html to markdown.')
    h = html2text.HTML2Text()
    if isinstance(text, unicode):
        logger.debug('Text is unicode.')
        return h.handle(text)
    logger.debug('Text is not unicode.')
    return h.handle(text.decode('utf-8', errors='ignore'))


def html2txtbs(text):
    logger.info('Converting html to txt with BS.')
    soup = BeautifulSoup(text, "lxml")
    return soup.get_text()


def html2txt(command, html_path):
    logger.info('Converting html to txt.')
    p = subprocess.call([command, 'build', html_path])
    return p

def write_text(path, filename, ext, text):
    filepath = join(path, filename + ext)
    logger.debug('Writing file %s', filepath)
    if type(text) is unicode:
        with open(filepath, 'w') as f:
            f.write(text.encode("UTF-8"))
    else:
        with open(filepath, 'w') as f:
            f.write(text)


def convert_dir(html_path, dst_path, convert_function, ext):
    if not isdir(dst_path):
        makedirs(dst_path)
    for html_file in listdir(html_path):
        filename, fileext = splitext(html_file)
        if fileext == '.html':
            logger.debug('Reading file %s', join(html_path, html_file))
            # with codecs.open(join(html_path, html_file), 'r', "utf-8") as fp:
            #     text = fp.read()
            with open(join(html_path, html_file), 'r') as f:
                text = f.read()
            converted_text = convert_function(text)
            write_text(dst_path, filename, ext, converted_text)
