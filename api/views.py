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
from flask import request, render_template, jsonify, g, flash, redirect, url_for, session, current_app, Response
from flask import json
from functools import wraps
from accounts.models import Organization
from decorators import api_key_required
from utils import cloud, get_provider_info
from nodes.models import NodeData
from bson import json_util
import re
from api import docs

bp = api_blueprint = Blueprint('api', __name__)

def generate_api_response(data, status=200, content_type='application/json'):
    indent = None
    if request.args.get('pretty'):
        indent = 2
    data = json.dumps(data, sort_keys=True, indent=indent, default=json_util.default)
    resp = Response(data, status=status, content_type=content_type)
    return resp

def load_provider_info(f):
    """
    Decorator that loads provider info into the session.  We use the session in order to return an
    error to the api consumer in the event the provider info is missing or incorrect.

    :param provider: Name of the provider
    :param account: Name of an account in the organization

    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # load provider info
        org = Organization.get_by_name(kwargs.get('organization'))
        org_name = None
        if org:
            org_name = org.name
        info = get_provider_info(kwargs.get('provider'), org_name, \
            kwargs.get('account'))
        session['provider_info'] = info
        # check for info ; if missing return error
        if not info.get('provider_id') or not info.get('provider_key'):
            data = {'error': 'Invalid or missing provider account information'}
            return generate_api_response(data, 400)
        return f(*args, **kwargs)
    return decorated

@bp.route('')
@api_key_required
def index():
    data = {
        'version': current_app.config.get('APP_VERSION'),
        'endpoints': [
            docs.nodes(),
        ]
    }
    return generate_api_response(data)

@bp.route('/<organization>/nodes/<account>/<provider>/<region>')
@api_key_required
@load_provider_info
def nodes(organization=None, account=None, provider=None, region=None):
    node_id = request.args.get('id', None)
    if node_id:
        node_id = [node_id]
    nodes = None
    account = request.args.get('account', session.get('default_account'))
    provider_info = session.get('provider_info')
    if provider_info.get('provider'):
        provider_id = provider_info.get('provider_id')
        provider_key = provider_info.get('provider_key')
        nodes = cloud.get_nodes(provider, region, provider_id, provider_key, node_ids=node_id)
    node_list = []
    for node in nodes:
        node_data = NodeData.get_by_node_id(node.id)
        if not node_data:
            node_data = NodeData()
        data = {
            'id': node.id,
            'uuid': node.uuid,
            'name': node.name,
            'image': node.image,
            'size': node.size,
            'extra': node.extra,
            'roles': node_data.roles,
        }
        node_list.append(data)
    data = {
        'account': account,
        'provider': provider,
        'region': region,
        'nodes': node_list,
    }
    return generate_api_response(data)