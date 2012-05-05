#!/usr/bin/env python
#    Copyright 2012 OpenCloud Project
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import os
from flask import Flask
from flask import json
import logging

APP_NAME = 'OpenCloud'
APP_VERSION = '0.1'
API_KEYS = (
    'defaultapikey',
)
CACHE_TYPE = 'simple'
LIBCLOUD_VERIFY_CERTS = False # defaults to false ; on mac os x with virtualenvs, cert checks fail
LOG_LEVEL = logging.DEBUG
# mongodb settings
MONGOALCHEMY_DATABASE = 'opencloud'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_EVENT_CHANNEL = 'opencloud'
SENTRY_DSN = None
SECRET_KEY='1q2w3e4r5t6y7u8i9o0p'

REGIONS = {
    'ec2': [
        {
            'name': 'us-east-1',
            'provider': 'ec2',
        },
        {
            'name': 'us-west-1',
            'provider': 'ec2',
        },
        {
            'name': 'us-west-2',
            'provider': 'ec2',
        },
        {
            'name': 'eu-west-1',
            'provider': 'ec2',
        },
    ],
    'rackspace': [
        {
            'name': 'DFW',
            'provider': 'rackspace',
        }
    ]
}

def create_app():
    """
    Flask app factory

    :rtype: `flask.Flask`

    """
    app = Flask(__name__)
    app.config.from_object('config')
    #sentry.init_app(app)
    return app

try:
    from local_config import *
except ImportError:
    pass