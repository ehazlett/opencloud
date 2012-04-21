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
from flaskext.mongoalchemy import MongoAlchemy
import config
from uuid import uuid4
import logging
from datetime import datetime

app = config.create_app()
db = MongoAlchemy(app)

class Log(db.Document):
    config_collection_name = 'logs'

    uuid = db.StringField(default=str(uuid4()))
    date = db.DateTimeField(default=datetime.now())
    level = db.IntField()
    name = db.StringField()
    message = db.StringField()

class MongoDBHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, msg):
        log = Log()
        log.level = msg.levelno
        log.name = msg.name
        log.message = msg.msg
        log.save()
        
def get_logger(name=''):
    log = logging.getLogger(name)
    log.setLevel(config.LOG_LEVEL)
    mongodb_handler = MongoDBHandler()
    mongodb_handler.setLevel(config.LOG_LEVEL)
    log.addHandler(mongodb_handler)
    return log