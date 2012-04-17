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
from flaskext.wtf import Form, TextField, SelectField, widgets, validators
from flaskext.babel import gettext

class LoginForm(Form):
    username = TextField(gettext('Username'), validators=[validators.Required()])
    password = TextField(gettext('Password'), validators=[validators.Required()], \
        widget=widgets.PasswordInput())

class AccountForm(Form):
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
