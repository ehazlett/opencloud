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

class Organization(db.Document):
    config_collection_name = 'accounts_organization'

    uuid = db.ComputedField(db.StringField(), lambda x: str(uuid4()), one_time=True)
    name = db.StringField()
    owner = db.StringField()
    api_key = db.StringField(default='')

    def update(self, **kwargs):
        # remove any key not in organization
        for k in kwargs.keys():
            if k not in self._fields.keys():
                kwargs.pop(k)
        q = self.query.filter_by(uuid=self.uuid).set(**kwargs)
        q.execute()

    @classmethod
    def get_by_name(self, name=None):
        return self.query.filter(Organization.name==name).first()

    @classmethod
    def get_by_api_key(self, api_key=None):
        return self.query.filter(Organization.api_key==api_key).first()

    @classmethod
    def get_by_uuid(self, uuid=None):
        return self.query.filter(Organization.uuid==uuid).first()

class Account(db.Document):
    config_collection_name = 'accounts_account'

    uuid = db.ComputedField(db.StringField(), lambda x: str(uuid4()), one_time=True)
    name = db.StringField()
    organization = db.StringField()
    provider = db.StringField()
    provider_id = db.StringField()
    provider_key = db.StringField()
    default_images = db.DictField(db.StringField(), required=False, default={})
    keypair = db.StringField(required=False, default='')

    def update(self, **kwargs):
        # remove any key not in account
        for k in kwargs.keys():
            if k not in self._fields.keys():
                kwargs.pop(k)
        q = self.query.filter_by(uuid=self.uuid).set(**kwargs)
        q.execute()

    @classmethod
    def get_by_uuid(self, uuid=None):
        return self.query.filter(Account.uuid==uuid).first()

class User(db.Document):
    config_collection_name = 'accounts_user'

    uuid = db.ComputedField(db.StringField(), lambda x: str(uuid4()), one_time=True)
    username = db.StringField(validator=username_validator)
    first_name = db.StringField(required=False, default='')
    last_name = db.StringField(required=False, default='')
    email = db.StringField(required=False, default='')
    password = db.StringField(required=False)
    roles = db.ListField(db.StringField(), required=False, default=[])
    active = db.BoolField(default=True)
    api_key = db.StringField(default='')
    organization = db.StringField(default='')

    def get_id(self):
        return self.uuid

    def is_admin(self):
        is_admin = False
        if 'admin' in self.roles:
            is_admin = True
        return is_admin

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
    def get_by_username(self, username=None, organization_id=None):
        return self.query.filter({'username': username, 'organization': organization_id}).first()

    @classmethod
    def get_by_uuid(self, uuid=None):
        return self.query.filter(User.uuid==uuid).first()

    @classmethod
    def get_by_api_key(self, api_key=None):
        return self.query.filter(User.api_key==api_key).first()
