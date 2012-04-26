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
from flaskext.wtf import Form, TextField, Field, TextInput, widgets, validators
from flaskext.babel import gettext

class TagListField(Field):
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
            
class ModuleForm(Form):
    name = TextField(gettext('Name'), validators=[validators.Required()])
    description = TextField(gettext('Description'), validators=[validators.Required()])
    content = TextField(gettext('Content'), widget=widgets.TextArea(), validators=[validators.Required()])
    tags = TagListField(gettext('Tags'))
    