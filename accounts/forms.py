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
from flaskext.wtf import Form, TextField, SelectField, Field, TextInput, widgets, validators
from flaskext.babel import gettext
from accounts.models import Organization, User

def get_organization_choices():
    organizations = Organization.query.all()
    choices = [(None, '-----')]
    for org in organizations:
        choices.append((org.uuid, org.name))
    return choices
    
def get_user_choices():
    users = User.query.all()
    choices = [(None, '-----')]
    for user in users:
        choices.append((user.uuid, user.username))
    return choices
    
class RoleListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return u' '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split()]
        else:
            self.data = []

class LoginForm(Form):
    username = TextField(gettext('Username'), validators=[validators.Required()])
    password = TextField(gettext('Password'), validators=[validators.Required()], \
        widget=widgets.PasswordInput())
    organization = TextField(gettext('Organization'))
    
class OrganizationForm(Form):
    name = TextField(gettext('Name'), validators=[validators.Required()])
    owner = SelectField(gettext('Owner'), choices=get_user_choices(), \
        validators=[validators.Required()])

class UserForm(Form):
    first_name = TextField(gettext('First name'), validators=[validators.Required()])
    last_name = TextField(gettext('Last name'), validators=[validators.Required()])
    email = TextField(gettext('Email'), validators=[validators.Required()])
    password = TextField(gettext('Password'), widget=widgets.PasswordInput(), validators=[
            validators.EqualTo('confirm_password', message=''),
    ])
    confirm_password = TextField(gettext('Password (confirm)'), \
        widget=widgets.PasswordInput(), validators=[
            validators.EqualTo('password', message=gettext('Passwords do not match')),
        ])
    api_key = TextField(gettext('API Key'))

class UserEditForm(Form):
    first_name = TextField(gettext('First name'), validators=[validators.Required()])
    last_name = TextField(gettext('Last name'), validators=[validators.Required()])
    email = TextField(gettext('Email'), validators=[validators.Required()])
    password = TextField(gettext('Password'), widget=widgets.PasswordInput(), validators=[
            validators.EqualTo('confirm_password', message=''),
    ])
    confirm_password = TextField(gettext('Password (confirm)'), \
        widget=widgets.PasswordInput(), validators=[
            validators.EqualTo('password', message=gettext('Passwords do not match')),
        ])
    organization = SelectField(gettext('Organization'), choices=get_organization_choices(), \
        validators=[validators.Required()])
    roles = RoleListField(gettext('Roles (space separated)'))
