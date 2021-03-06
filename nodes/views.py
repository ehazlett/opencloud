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
from flaskext.cache import Cache
import messages
from utils import cloud, get_provider_info
import config
from nodes.models import NodeData
from accounts.models import Organization, Account

bp = nodes_blueprint = Blueprint('nodes', __name__)
app = config.create_app()
cache = Cache(app)

@bp.route('/')
@bp.route('/<region>')
@login_required
def index(region=None):
    regions = []
    provider = None
    account_data = Account.query.filter({'organization': session.get('organization').uuid, 'name': session.get('default_account')}).first()
    if account_data:
        provider = account_data.provider
        if current_app.config.get('REGIONS').get(provider):
            regions = [x.get('name') for x in current_app.config.get('REGIONS').get(provider)]
    ctx = {
        'provider': provider,
        'regions': regions,
        'region': region,
    }
    return render_template('nodes/index.html', **ctx)

@bp.route('/<provider>/<region>/')
@login_required
def nodes(provider=None, region=None):
    account = request.args.get('account', session.get('default_account'))
    nodes = None
    provider_info = get_provider_info(provider, session.get('organization').name, account)
    if provider_info.get('provider'):
        provider_id = provider_info.get('provider_id')
        provider_key = provider_info.get('provider_key')
        nodes = cloud.get_nodes(provider, region, provider_id, provider_key)
    ctx = {
        'provider': provider,
        'region': region,
        'nodes': nodes,
    }
    return render_template('nodes/_nodes.html', **ctx)

@bp.route('/<provider>/<region>/<node_id>/reboot')
@login_required
def node_reboot(provider=None, region=None, node_id=None):
    account = request.args.get('account', session.get('default_account'))
    provider_info = get_provider_info(provider, session.get('organization').name, account)
    if provider_info.get('provider'):
        provider_id = provider_info.get('provider_id')
        provider_key = provider_info.get('provider_key')
        cloud.reboot_node(provider, region, provider_id, provider_key, node_id)
        flash(messages.INSTANCE_REBOOTED)
        current_app.logger.info('{0} ({1}) rebooted node {2} in {3} ({4})'.format(session.get('user').username, \
            session.get('organization').name, node_id, provider, region))
    return redirect(url_for('nodes.index', region=region))

@bp.route('/<provider>/<region>/<node_id>/stop')
@login_required
def node_stop(provider=None, region=None, node_id=None):
    account = request.args.get('account', session.get('default_account'))
    provider_info = get_provider_info(provider, session.get('organization').name, account)
    if provider_info.get('provider'):
        provider_id = provider_info.get('provider_id')
        provider_key = provider_info.get('provider_key')
        if cloud.stop_node(provider, region, provider_id, provider_key, node_id):
            flash(messages.INSTANCE_STOPPED)
            current_app.logger.info('{0} ({1}) stopped node {2} in {3} ({4})'.format(session.get('user').username, \
                session.get('organization').name, node_id, provider, region))
    return redirect(url_for('nodes.index', region=region))

@bp.route('/<provider>/<region>/<node_id>/destroy')
@login_required
def node_destroy(provider=None, region=None, node_id=None):
    account = request.args.get('account', session.get('default_account'))
    provider_info = get_provider_info(provider, session.get('organization').name, account)
    if provider_info.get('provider'):
        provider_id = provider_info.get('provider_id')
        provider_key = provider_info.get('provider_key')
        cloud.destroy_node(provider, region, provider_id, provider_key, node_id)
        flash(messages.INSTANCE_DESTROYED)
        current_app.logger.info('{0} ({1}) destroyed node {2} in {3} ({4})'.format(session.get('user').username, \
            session.get('organization').name, node_id, provider, region))
    return redirect(url_for('nodes.index', region=region))

@bp.route('/<provider>/<region>/launch', methods=['GET', 'POST'])
@login_required
def node_launch(provider=None, region=None):
    nodes = None
    account = request.args.get('account', session.get('default_account'))
    provider_info = get_provider_info(provider, session.get('organization').name, account)
    if provider_info.get('provider'):
        provider_id = provider_info.get('provider_id')
        provider_key = provider_info.get('provider_key')
    if request.method == 'POST':
        node_name = request.form.get('name')
        node_image_id = request.form.get('image')
        node_size_id = request.form.get('size')
        keypair = request.form.get('keypair', None)
        security_groups = request.form.get('security_groups', None)
        try:
            cloud.launch_node(provider, region, provider_id, provider_key, node_name, \
                node_image_id, node_size_id, keypair=keypair, security_groups=security_groups)
            current_app.logger.info('{0} ({1}) launched node {2} ({3}) in {4} ({5})'.format(session.get('user').username, \
                session.get('organization').name, node_name, node_image_id, provider, region))
            flash(messages.INSTANCE_LAUNCHED)
        except Exception, e:
            flash(e, 'error')
        return redirect(url_for('nodes.index', region=region))
    default_images = [x for x in provider_info.get('provider_data', {}).get('default_images', None) if x.get('region') == region]
    ctx = {
        'provider': provider,
        'provider_info': provider_info,
        'region': region,
        'images': cloud.get_images(provider, region, provider_id, provider_key),
        'sizes': cloud.get_sizes(provider, region, provider_id, provider_key),
        'keypair': provider_info.get('provider_data', {}).get('keypair'),
        'default_images': default_images,
    }
    return render_template('nodes/_launch_server.html', **ctx)

@bp.route('/<provider>/<region>/<node_id>/roles')
@login_required
def node_roles(provider=None, region=None, node_id=None):
    account = request.args.get('account', session.get('default_account'))
    provider_info = get_provider_info(provider, session.get('organization').name, account)
    node_data = None
    if provider_info.get('provider'):
        provider_id = provider_info.get('provider_id')
        provider_key = provider_info.get('provider_key')
        node_data = NodeData.get_by_node_id(node_id)
        if not node_data:
            node_data = NodeData()
            node_data.node_id = node_id
            node_data.save()
    ctx = {
        'provider': provider,
        'provider_info': provider_info,
        'region': region,
        'node_id': node_id,
        'node_data': node_data,
    }
    return render_template('nodes/_node_roles.html', **ctx)

@bp.route('/<provider>/<region>/<node_id>/roles/set', methods=['POST'])
@login_required
def node_set_roles(provider=None, region=None, node_id=None):
    account = request.args.get('account', session.get('default_account'))
    provider_info = get_provider_info(provider, session.get('organization').name, account)
    node_data = None
    roles = request.form.get('roles', '').split()
    if provider_info.get('provider'):
        provider_id = provider_info.get('provider_id')
        provider_key = provider_info.get('provider_key')
        node_data = NodeData.get_by_node_id(node_id)
        node_data.roles = roles
        node_data.save()
        current_app.logger.info('{0} ({1}) updated roles for node {2} in {3} ({4}): {5}'.format(session.get('user').username, \
            session.get('organization').name, node_id, provider, region, roles))
        flash(messages.NODE_ROLES_UPDATED)
    return redirect(url_for('nodes.index', region=region))