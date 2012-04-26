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
from datetime import datetime

app = create_app()
db = MongoAlchemy(app)

class Module(db.Document):
    config_collection_name = 'modules'

    uuid = db.StringField()
    created = db.DateTimeField()
    author = db.StringField()
    name = db.StringField()
    description = db.StringField(required=False)
    content = db.StringField(required=False)
    enabled = db.BoolField(default=True)
    tags = db.ListField(db.StringField(), required=False, default=[])

    def update(self, **kwargs):
        # remove any key not in module
        for k in kwargs.keys():
            if k not in self._fields.keys():
                kwargs.pop(k)
        q = self.query.filter_by(uuid=self.uuid).set(**kwargs)
        q.execute()

    @classmethod
    def get_by_uuid(self, uuid=None):
        return self.query.filter(Module.uuid==uuid).first()
    