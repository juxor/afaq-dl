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

# repo
DATA_REMOTE_REPO = {'name': 'githubjuxor',
                    'url': 'https://github.com/juxor/afaq',
                    'branch': 'master'}
METADATA_FILE = 'metadata.yml'
GIT_AUTHOR_NAME = 'afaq scraper'
GIT_AUTHOR_EMAIL = 'ju@riseup.net'

# FS paths
TXT_BS_DIR = 'txtbs'
MD_DIR = 'markdown'
HTML2TXT_SCRIPT = 'html2txt'

# ssh
MORPH_SSH_PRIV_KEY_ENV = 'MORPH_SSH_PRIV_KEY'
MORPH_SSH_PUB_KEY_ENV = 'MORPH_SSH_PUB_KEY'
SSH_DIR = 'ssh'
GIT_SSH_COMMAND_FILE = 'ssh_command.sh'
GITHUB_SSH_PUB_KEY = 'github.com ssh-rsa xxx'

# FS paths created from the constants
from os.path import abspath, dirname, join
from afaq_scraper.settings import DATA_LOCAL_REPO_PATH, DATA_REPO_DIR

BASE_PATH = dirname(abspath(__file__))
ROOT_PATH = dirname(BASE_PATH)

# FIXME: only for DEBUG!
# DATA_REMOTE_REPO = {'name': 'local',
#                     'url': 'file://%s' % join(dirname(ROOT_PATH),
#                                               DATA_REPO_DIR),
#                     'branch': 'master'}
print(DATA_REMOTE_REPO.get('url'))
METADATA_PATH = join(DATA_LOCAL_REPO_PATH, METADATA_FILE)

TXT_BS_PATH = join(DATA_LOCAL_REPO_PATH, TXT_BS_DIR)
MD_PATH = join(DATA_LOCAL_REPO_PATH, MD_DIR)
HTML2TXT_COMMAND = join(BASE_PATH, HTML2TXT_SCRIPT)

# ssh
SSH_PATH = join(ROOT_PATH, SSH_DIR)
SSH_PRIV_KEY_PATH = join(SSH_PATH, 'id_rsa')
SSH_PUB_KEY_PATH = join(SSH_PATH, 'id_rsa.pub')
GIT_SSH_COMMAND_PATH = join(SSH_PATH, GIT_SSH_COMMAND_FILE)

SSH_PUB_KEY_SERVER_PATH = join(SSH_PATH, 'ssh_pub_key_server')

GIT_SSH_COMMAND = '#!/bin/sh\nssh -i ' + SSH_PRIV_KEY_PATH + \
    ' -o "UserKnownHostsFile ' + SSH_PUB_KEY_SERVER_PATH + \
    '" "$@"\n'

GIT_SSH_COMMAND_MORPHIO = '#!/bin/sh\nssh -i ' + SSH_PRIV_KEY_PATH + \
    ' -o "UserKnownHostsFile ' + SSH_PUB_KEY_SERVER_PATH + \
    '" -o "StrictHostKeyChecking no"' + \
    ' "$@"\n'

try:
    from config_local import *
except:
    pass
