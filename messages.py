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
from flaskext.babel import gettext

ACCESS_DENIED = gettext('Access denied.')
ACCOUNT_UPDATED = gettext('Account updated.')
INVALID_API_KEY = gettext('Invalid API key')
INVALID_USERNAME_OR_PASSWORD = gettext('Invalid username/password')
LOGGED_IN = gettext('Welcome back...!')
LOGGED_OUT = gettext('You have been logged out.')
NO_API_KEY = gettext('No API key specified')