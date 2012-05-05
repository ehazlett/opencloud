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
from flask import current_app, session, request

def hash_password(password=None):
    try:
        salt = current_app.config.get('SECRET_KEY')
    except RuntimeError:
        import config
        salt = config.SECRET_KEY
    h = hashlib.sha256(salt)
    h.update(password)
    return h.hexdigest()

def get_provider_info(provider=None, organization=None):
    data = {}
    if not organization:
        organization = request.args.get('organization', session.get('default_organization'))
    org_data = current_app.config.get('APP_CONFIG').get('organizations').get(organization)
    provider_id = None
    provider_key = None
    provider_data = None
    if org_data:
        provider_id = org_data.get('provider_id')
        provider_key = org_data.get('provider_key')
        provider_data = org_data.get('provider_data')
    data.update(
        provider = provider,
        provider_id = provider_id,
        provider_key = provider_key,
        provider_data = provider_data
    )
    return data