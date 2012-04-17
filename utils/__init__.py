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
import hashlib
from flask import current_app

def hash_password(password=None):
    try:
        salt = current_app.config.get('SECRET_KEY')
    except RuntimeError:
        import config
        salt = config.SECRET_KEY
    h = hashlib.sha256(salt)
    h.update(password)
    return h.hexdigest()