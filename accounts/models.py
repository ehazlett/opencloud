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
import string
import utils
from flask import current_app

app = create_app()
db = MongoAlchemy(app)

def username_validator(username):
    allowed_chars = string.letters + string.digits + '@' + '.'
    retval = True
    for c in str(username):
        if c not in allowed_chars:
            retval = False
            break
    # TODO: check if username exists
    return retval

class User(db.Document):
    config_collection_name = 'users'

    uuid = db.StringField(default=str(uuid4()))
    username = db.StringField(validator=username_validator)
    first_name = db.StringField(required=False, default='')
    last_name = db.StringField(required=False, default='')
    email = db.StringField(required=False, default='')
    password = db.StringField(required=False)
    roles = db.ListField(db.StringField(), required=False, default=[])
    active = db.BoolField(default=True)
    state = db.StringField(required=False, default='')

    def get_id(self):
        return self.uuid

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_roles(self):
        return self.roles

    def add_role(self, role=None):
        if role not in self.roles:
            self.roles.append(role)
        return True

    def remove_role(self, role=None):
        if role in self.roles:
            self.roles.remove(role)
        return True

    def set_password(self, password=None):
        self.password = utils.hash_password(password)
        return True

    def update(self, **kwargs):
        # remove any key not in user
        for k in kwargs.keys():
            if k not in self._fields.keys():
                kwargs.pop(k)
        # look for password and set
        if 'password' in kwargs:
            if kwargs['password'].strip() != '':
                self.set_password(kwargs['password'])
                self.save()
            kwargs.pop('password')
        q = self.query.filter_by(uuid=self.uuid).set(**kwargs)
        q.execute()

    @classmethod
    def get_by_username(self, username=None):
        return self.query.filter(User.username==username).first()

    @classmethod
    def get_by_uuid(self, uuid=None):
        return self.query.filter(User.uuid==uuid).first()
