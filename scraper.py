#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab

# Copyright 2016 juxor <ju@riseup.net>

# This file is part of afaq-dl.
#
# afaq-dl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# afaq-dl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with afaq-dl.  If not, see <http://www.gnu.org/licenses/>.

""""""
import os
import sys
import argparse
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from scrapy.utils.log import configure_logging

here = os.path.abspath(os.path.dirname(__file__))
path, directory = os.path.split(os.path.realpath(here))
if directory == 'bin':
    sys.path.insert(0, path)

from afaqdl.utils import convert, git_utils, system
from afaqdl import conf
from afaqdl import version


def main():
    settings = get_project_settings()

    parser = argparse.ArgumentParser()
    parser.add_argument('-d',
                        '--debug',
                        help='Set logging level to debug',
                        action='store_true')
    parser.add_argument('-v', '--version', action='version',
                        help='version',
                        version='%(prog)s ' + version)
    parser.add_argument('-o', '--outputdir',
                        help='output local path',
                        default=conf.DATA_LOCAL_REPO_PATH)
    parser.add_argument('-c', '--crawl',
                        help='Crawl AFAQ.',
                        action='store_true')
    parser.add_argument('-g', '--pull',
                        help='Pull git repo before obtaining AFAQ.',
                        action='store_true')
    parser.add_argument('-p', '--push',
                        help='Push to git repo AFAQ changes.',
                        action='store_true')
    parser.add_argument('-r', '--rm',
                        help='Remove content outputdir before crawling.',
                        action='store_true')
    parser.add_argument('-m', '--convert',
                        help='Convert obtained AFAQ to other formats.',
                        action='store_true')
    parser.add_argument('-a', '--all',
                        help='Equivalent to -g, -c, -p, -r, -m.',
                        action='store_true',
                        default=True)

    args = parser.parse_args()
    if args.all is True:
        args.pull = args.crawl = args.push = args.convert = args.rm = \
            args.debug = True

#    configure_logging()
    logging.basicConfig(format=conf.LOG_FORMAT)
    logging.getLogger('scrapy').propagate = False
    logger = logging.getLogger('root')
    logger.propagate = True

    if args.debug is True:
        logger.setLevel(logging.DEBUG)
#        settings.set('DEBUG', True)
#        conf.DEBUG = True

    if args.pull is True:
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
        git_utils.write_ssh_key_server(conf.GITLAB_SSH_PUB_KEY,
                                       conf.SSH_PUB_KEY_SERVER_PATH)

        # Pull or clone the data repos
        logger.debug('Remote repo name %s' %
                     conf.DATA_REMOTE_REPO.get('name'))
        local_repo, remote_repo = git_utils.obtain_repo(
                                    conf.DATA_LOCAL_REPO_PATH,
                                    conf.DATA_REMOTE_REPO,
                                    conf.GIT_SSH_COMMAND_PATH,
                                    False
                                  )
    if args.rm is True:
        # rm files in case they are deleted in the sources
        # TODO: if this is removed then the files removed should be
        # detected on git commit
        system.rm_data(conf.DATA_LOCAL_REPO_PATH)

    if args.crawl is True:
        # Run the scraper
        process = CrawlerProcess(settings)
        process.crawl('afaq')
        process.start()
        process.stop()

    if args.convert is True:
        # Conversions
        convert.convert_dir(conf.HTML_PATH, conf.MD_PATH,
                            convert.html2md, '.md')
        # NOTE: since there is already md, txt is not needed
        #convert.html2txt(conf.HTML2TXT_COMMAND, conf.HTML_PATH)

    if args.push is True:
        # Push the scraped data in the repos
        git_utils.commit_push_if_changes(local_repo,
                                         conf.GIT_AUTHOR_NAME,
                                         conf.GIT_AUTHOR_EMAIL,
                                         conf.GIT_SSH_COMMAND_PATH,
                                         conf.DATA_REMOTE_REPO,
                                         conf.METADATA_PATH)

if __name__ == '__main__':
    main()
