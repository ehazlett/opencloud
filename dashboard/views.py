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
from flask import Blueprint
from flask import request, render_template, jsonify, g, flash, redirect, url_for, session, current_app
from flaskext.login import login_required
import messages
from utils import cloud

bp = dashboard_blueprint = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    ctx = {
        'regions': current_app.config.get('REGIONS'),
    }
    return render_template('dashboard/index.html', **ctx)
    
@bp.route('/nodes')
def nodes():
    org = request.args.get('organization', session.get('default_organization'))
    org_data = current_app.config.get('APP_CONFIG').get('organizations').get(org)
    provider = request.args.get('provider', org_data.get('provider'))
    provider_id = org_data.get('provider_id')
    provider_key = org_data.get('provider_key')
    ctx = {
        'provider': provider,
        'nodes': cloud.get_nodes(provider, provider_id, provider_key),
    }
    return render_template('dashboard/nodes.html', **ctx)