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
from functools import wraps
from flask import request, current_app, redirect
from flask import jsonify
from flask import url_for
from flask import flash
from flask import session
from accounts.models import User
import messages

def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = None
        if 'apikey' in request.form:
            api_key = request.form.get('apikey')
        elif 'X-Api-Key' in request.headers.keys():
            api_key = request.headers.get('X-Api-Key')
        # validate
        if not api_key:
            data = {'error': messages.NO_API_KEY}
            return jsonify(data)
        user = User.get_by_api_key(api_key=api_key)
        if not user and api_key not in current_app.config.get('API_KEYS', []):
            data = {'error': messages.INVALID_API_KEY}
            return jsonify(data)
        # check that user is active
        if user:
            session['user'] = user
            if not user.active:
                data = {'error': messages.ACCOUNT_INACTIVE}
                return jsonify(data)
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # check for admin role
        user = session.get('user', None)
        if not user or 'admin' not in user.roles:
            flash(messages.ACCESS_DENIED, 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

def organization_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # check for organization
        if not request.args.get('organization'):
            data = {'error': messages.ORGANIZATION_REQUIRED}
            return jsonify(data)
        return f(*args, **kwargs)
    return decorated

def provider_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # check for provider
        if not request.args.get('provider'):
            data = {'error': messages.PROVIDER_REQUIRED}
            return jsonify(data)
        return f(*args, **kwargs)
    return decorated

def region_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # check for region
        if not request.args.get('region'):
            data = {'error': messages.REGION_REQUIRED}
            return jsonify(data)
        return f(*args, **kwargs)
    return decorated
