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

def get_provider_info():
    data = {}
    org = request.args.get('organization', session.get('default_organization'))
    org_data = current_app.config.get('APP_CONFIG').get('organizations').get(org)
    provider = None
    provider_id = None
    provider_key = None
    if org_data:
        provider = request.args.get('provider', org_data.get('provider'))
        provider_id = org_data.get('provider_id')
        provider_key = org_data.get('provider_key')
    data.update(
        provider = provider,
        provider_id = provider_id,
        provider_key = provider_key
    )
    return data
    
@bp.route('/')
@login_required
def index():
    regions = []
    org_data = current_app.config.get('APP_CONFIG').get('organizations').get(session.get('default_organization'))
    if org_data:
        provider = org_data.get('provider')
        regions = current_app.config.get('REGIONS').get(provider)
    ctx = {
        'regions': regions,
    }
    return render_template('dashboard/index.html', **ctx)
    
@bp.route('/nodes/')
@login_required
def nodes():
    org = request.args.get('organization', session.get('default_organization'))
    provider = None
    regions = None
    nodes = None
    provider_info = get_provider_info()
    if provider_info.get('provider'):
        provider = provider_info.get('provider')
        provider_id = provider_info.get('provider_id')
        provider_key = provider_info.get('provider_key')
        regions = current_app.config.get('REGIONS').get(provider)
        nodes = cloud.get_nodes(provider, provider_id, provider_key)
    ctx = {
        'provider': provider,
        'regions': regions,
        'nodes': nodes,
    }
    return render_template('dashboard/nodes.html', **ctx)

@bp.route('/nodes/<node_id>/reboot')
@login_required
def node_reboot(node_id=None):
    org = request.args.get('organization', session.get('default_organization'))
    provider_info = get_provider_info()
    if provider_info.get('provider'):
        provider = provider_info.get('provider')
        provider_id = provider_info.get('provider_id')
        provider_key = provider_info.get('provider_key')
        cloud.reboot_node(provider, provider_id, provider_key, node_id)
        flash(messages.INSTANCE_REBOOTED)
    return redirect(url_for('dashboard.index'))
        
        