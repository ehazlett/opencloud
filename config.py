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

APP_CONFIG = {}
APP_NAME = 'OpenCloud'
APP_VERSION = '0.1'
API_KEYS = (
    'defaultapikey',
)
LIBCLOUD_VERIFY_CERTS = False # defaults to false ; on mac os x with virtualenvs, cert checks fail
LOCAL_CONFIG = 'config_local.json'
MASTER_CONFIG = 'config.json'
# mongodb settings
MONGOALCHEMY_DATABASE = 'opencloud'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 12
REDIS_EVENT_CHANNEL = 'opencloud'
SENTRY_DSN = None
SECRET_KEY='1q2w3e4r5t6y7u8i9o0p'

REGIONS = [
    {
        'provider': 'ec2',
        'name': 'us-east-1'
    },
    {
        'provider': 'ec2',
        'name': 'us-west-1'
    },
    {
        'provider': 'ec2',
        'name': 'us-west-2'
    },
    {
        'provider': 'ec2',
        'name': 'eu-west-1'
    },
    #{
    #    'provider': 'ec2',
    #    'name': 'ap-southeast-1'
    #},
    #{
    #    'provider': 'ec2',
    #    'name': 'ap-southeast-2'
    #}
]

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

if os.path.exists(MASTER_CONFIG):
    with open(MASTER_CONFIG, 'r') as f:
        APP_CONFIG = json.loads(f.read())

if os.path.exists(LOCAL_CONFIG):
    with open(LOCAL_CONFIG, 'r') as f:
        LOCAL_CONFIG = json.loads(f.read())

# merge local and master configs
for k,v in LOCAL_CONFIG.iteritems():
    if isinstance(LOCAL_CONFIG[k], dict):
        for x, y in LOCAL_CONFIG[k].iteritems():
            APP_CONFIG[k][x] = y
    else:
        APP_CONFIG[k] = v
