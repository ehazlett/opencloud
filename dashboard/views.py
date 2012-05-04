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
from utils import cloud
import config

bp = dashboard_blueprint = Blueprint('dashboard', __name__)
app = config.create_app()
cache = Cache(app)

def get_provider_info(provider=None):
    data = {}
    org = request.args.get('organization', session.get('default_organization'))
    org_data = current_app.config.get('APP_CONFIG').get('organizations').get(org)
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

@bp.route('/')
@bp.route('/<region>')
@login_required
def index(region=None):
    regions = []
    provider = None
    org_data = current_app.config.get('APP_CONFIG').get('organizations').get(session.get('default_organization'))
    if org_data:
        provider = org_data.get('provider')
        if current_app.config.get('REGIONS').get(provider):
            regions = [x.get('name') for x in current_app.config.get('REGIONS').get(provider)]
    ctx = {
        'provider': provider,
        'regions': regions,
        'region': region,
    }
    return render_template('dashboard/index.html', **ctx)

@bp.route('/nodes/<provider>/<region>/')
@login_required
def nodes(provider=None, region=None):
    org = request.args.get('organization', session.get('default_organization'))
    nodes = None
    provider_info = get_provider_info(provider)
    if provider_info.get('provider'):
        provider_id = provider_info.get('provider_id')
        provider_key = provider_info.get('provider_key')
        nodes = cloud.get_nodes(provider, region, provider_id, provider_key)
    ctx = {
        'provider': provider,
        'region': region,
        'nodes': nodes,
    }
    return render_template('dashboard/_nodes.html', **ctx)

@bp.route('/nodes/<provider>/<region>/<node_id>/reboot')
@login_required
def node_reboot(provider=None, region=None, node_id=None):
    org = request.args.get('organization', session.get('default_organization'))
    provider_info = get_provider_info(provider)
    if provider_info.get('provider'):
        provider_id = provider_info.get('provider_id')
        provider_key = provider_info.get('provider_key')
        cloud.reboot_node(provider, region, provider_id, provider_key, node_id)
        flash(messages.INSTANCE_REBOOTED)
        current_app.logger.info('{0} rebooted node {1} in {2} ({3})'.format(session.get('user').username, \
            node_id, provider, region))
    return redirect(url_for('dashboard.index', region=region))

@bp.route('/nodes/<provider>/<region>/<node_id>/stop')
@login_required
def node_stop(provider=None, region=None, node_id=None):
    org = request.args.get('organization', session.get('default_organization'))
    provider_info = get_provider_info(provider)
    if provider_info.get('provider'):
        provider_id = provider_info.get('provider_id')
        provider_key = provider_info.get('provider_key')
        if cloud.stop_node(provider, region, provider_id, provider_key, node_id):
            flash(messages.INSTANCE_STOPPED)
            current_app.logger.info('{0} stopped node {1} in {2} ({3})'.format(session.get('user').username, \
                node_id, provider, region))
    return redirect(url_for('dashboard.index', region=region))

@bp.route('/nodes/<provider>/<region>/<node_id>/destroy')
@login_required
def node_destroy(provider=None, region=None, node_id=None):
    org = request.args.get('organization', session.get('default_organization'))
    provider_info = get_provider_info(provider)
    if provider_info.get('provider'):
        provider_id = provider_info.get('provider_id')
        provider_key = provider_info.get('provider_key')
        cloud.destroy_node(provider, region, provider_id, provider_key, node_id)
        flash(messages.INSTANCE_DESTROYED)
        current_app.logger.info('{0} destroyed node {1} in {2} ({3})'.format(session.get('user').username, \
            node_id, provider, region))
    return redirect(url_for('dashboard.index', region=region))

@bp.route('/nodes/<provider>/<region>/launch', methods=['GET', 'POST'])
@login_required
def node_launch(provider=None, region=None):
    org = request.args.get('organization', session.get('default_organization'))
    nodes = None
    provider_info = get_provider_info(provider)
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
            current_app.logger.info('{0} launched node {1} ({2}) in {3} ({4})'.format(session.get('user').username, \
                node_name, node_image_id, provider, region))
            flash(messages.INSTANCE_LAUNCHED)
        except Exception, e:
            flash(e, 'error')
        return redirect(url_for('dashboard.index', region=region))
    default_images = provider_info.get('provider_data').get('images', {}).get(region, None)
    ctx = {
        'provider': provider,
        'provider_info': provider_info,
        'region': region,
        'images': cloud.get_images(provider, region, provider_id, provider_key),
        'sizes': cloud.get_sizes(provider, region, provider_id, provider_key),
        'default_images': default_images,
    }
    return render_template('dashboard/_launch_server.html', **ctx)