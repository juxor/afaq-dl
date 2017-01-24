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

import logging
import hashlib
from pkg_resources import get_distribution, DistributionNotFound
from os import uname
from os.path import expanduser
from os import environ
from os import listdir
import socket
from urllib2 import urlopen
from datetime import datetime
import yaml

logger = logging.getLogger(__name__)


def generate_hash(text):
    sha = hashlib.sha256(text).hexdigest()
    logger.debug(sha)
    return sha


def obtain_script_version():
    try:
        _dist = get_distribution('afaq-scraper')
    except DistributionNotFound:
        __version__ = 'Please install this project with setup.py'
    else:
        __version__ = _dist.version
    logger.debug(__version__)


def obtain_script_commit_hash(script_path):
    from git import Repo, GitCmdObjectDB
    # FIXME: ROOT_PATH
    script_repo = Repo(script_path, odbt=GitCmdObjectDB)
    commit_hash = script_repo.head.commit.hexsha
    logger.debug(commit_hash)
    return commit_hash

def obtain_uname():
    kernel_version = ' '.join(uname())
    logger.debug(kernel_version)
    return kernel_version


def obtain_home():
    home = expanduser('~')
    logger.debug('home %s' % home)
    return home


def obtain_environ():
    logger.debug('environ %s' % environ)
    return environ


def ls(dir_path):
    ls = listdir(dir_path)
    logger.debug('ls %s' % ls)
    return ls


def generate_host_identifier():
    hostid = generate_hash(obtain_uname())
    logger.debug(hostid)
    return hostid


def obtain_ip():
    ip = socket.gethostbyname(socket.gethostname())
    logger.debug('ip %s' % ip)
    return ip


def obtain_public_ip():
    my_ip = urlopen('http://ip.42.pl/raw').read()
    logger.debug('public ip %s' % my_ip)
    return str(my_ip)


def now():
    now = datetime.now()
    logger.debug(now)
    return now


def ismorpio():
    if environ['HOME'] == '/app':
        logger.debug('running in morph.io')
        return True
    logger.debug('not running in morph.io')
    return False


def hasproxy():
    # FIXME: http proxy might not change the public address,
    # assuming it does for now
    if environ.get('HTTP_PROXY'):
        logger.debug('there is an HTTP_PROXY')
        return True
    logger.debug('there is not an HTTP_PROXY')
    return False


def generate_metadata(local_repo_path):
    # ADVICE: system information is sensitive
    # in morph.io or running with tor, the ip will change all the time
    # FIXME: in morph.io cant obtain the current git revision this way
    # in morph.io host name will change all the time
    # an env variable that doesnt change is HOME=/app
    if ismorpio():
        ip = obtain_public_ip()
        uname = obtain_uname()
        commit_revision = None
        host = 'morph.io'
    elif hasproxy():
        ip = obtain_public_ip()
        uname = generate_hash(obtain_uname())
        commit_revision = obtain_script_commit_hash(local_repo_path)
        host = 'local'
    else:
        ip = generate_hash(obtain_public_ip())
        uname = generate_hash(obtain_uname())
        commit_revision = obtain_script_commit_hash(local_repo_path)
        host = 'dev server'
        metadata = {
            'timestamp': str(now()),
            'ip': ip,
            'uname': uname,
            'commit_revision': commit_revision,
            'host': host
        }
    logger.debug(metadata)
    return metadata


def write_metadata_file(metadata_path, local_repo_path):
    metadata = generate_metadata(local_repo_path)
    metadata_yaml = generate_yaml(metadata)
    with open(metadata_path, 'w') as f:
        f.write(metadata_yaml)
        logger.debug('wroten %s with %s' % (metadata_path, metadata_yaml))


def generate_metadata(local_repo_path):
    # ADVICE: system information is sensitive
    # in morph.io or running with tor, the ip will change all the time
    # FIXME: in morph.io cant obtain the current git revision this way
    # in morph.io host name will change all the time
    # an env variable that doesnt change is HOME=/app
    if ismorpio():
        ip = obtain_public_ip()
        uname = obtain_uname()
        commit_revision = None
        host = 'morph.io'
    elif hasproxy():
        ip = obtain_public_ip()
        uname = generate_hash(obtain_uname())
        commit_revision = obtain_script_commit_hash(local_repo_path)
        host = 'local'
    else:
        ip = generate_hash(obtain_public_ip())
        uname = generate_hash(obtain_uname())
        commit_revision = obtain_script_commit_hash(local_repo_path)
        host = 'dev server'
    metadata = {
        'timestamp': str(now()),
        'ip': ip,
        'uname': uname,
        'commit_revision': commit_revision,
        'host': host
    }
    logger.debug(metadata)
    return metadata


def generate_yaml(dict_data):
    data_yaml = yaml.safe_dump(dict_data)
    logger.debug(data_yaml)
    return data_yaml
