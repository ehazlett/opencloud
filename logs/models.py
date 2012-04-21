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
from config import create_app
from uuid import uuid4
from datetime import datetime

app = create_app()
db = MongoAlchemy(app)

class Log(db.Document):
    config_collection_name = 'logs'

    uuid = db.StringField(default=str(uuid4()))
    date = db.DateTimeField(default=datetime.now())
    level = db.IntField()
    name = db.StringField()
    message = db.StringField()