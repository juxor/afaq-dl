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
import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from utils import convert, git_utils, system
import conf
from afaq_scraper import settings

from afaq_scraper.spiders import afaq

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=settings.LOG_LEVEL,
                        format=settings.LOG_FORMAT,
                        datefmt=settings.LOG_DATEFORMAT)

    # Write ssh keys and command neede for git_utils
    if not os.path.isdir(conf.SSH_PATH):
        os.makedirs(conf.SSH_PATH)
        logger.debug('Created ssh dir: %s.', conf.SSH_PATH)
    if system.ismorpio():
        git_utils.write_ssh_keys(conf.SSH_DIR,
                                 conf.MORPH_SSH_PRIV_KEY_ENV,
                                 conf.MORPH_SSH_PUB_KEY_ENV,
                                 conf.SSH_PRIV_KEY_PATH,
                                 conf.SSH_PUB_KEY_PATH)
        git_utils.write_ssh_command(conf.GIT_SSH_COMMAND_PATH,
                                    conf.GIT_SSH_COMMAND_MORPHIO)
    else:
        git_utils.write_ssh_command(conf.GIT_SSH_COMMAND_PATH,
                                    conf.GIT_SSH_COMMAND)
    git_utils.write_ssh_key_server(conf.GITHUB_SSH_PUB_KEY,
                                   conf.SSH_PUB_KEY_SERVER_PATH)

    # Pull or clone the data repos
    logger.debug('Remote repo name %s' % conf.DATA_REMOTE_REPO.get('name'))
    local_repo, remote_repo = git_utils.obtain_repo(
                                settings.DATA_LOCAL_REPO_PATH,
                                conf.DATA_REMOTE_REPO,
                                conf.GIT_SSH_COMMAND_PATH,
                                False
                              )

    # Run the scraper
    configure_logging()
    process = CrawlerProcess(get_project_settings())
    process.crawl('afaq')
    process.start()
    process.stop()

    # Conversions
    convert.convert_dir(settings.HTML_PATH, conf.MD_PATH,
                        convert.html2md, '.md')

    # Push the scraped data in the repos
    git_utils.commit_push_if_changes(local_repo,
                                     conf.GIT_AUTHOR_NAME,
                                     conf.GIT_AUTHOR_EMAIL,
                                     conf.GIT_SSH_COMMAND_PATH,
                                     conf.DATA_REMOTE_REPO,
                                     conf.METADATA_PATH)

if __name__ == '__main__':
    main()
