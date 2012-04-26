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
from modules.models import Module
from modules.forms import ModuleForm
import messages
import re
from uuid import uuid4
from datetime import datetime

bp = modules_blueprint = Blueprint('modules', __name__)

@bp.route('/')
@login_required
def index():
    count = int(request.args.get('count', 15))
    page = int(request.args.get('page', 1))
    query = request.args.get('search', None)
    if query:
        regex = re.compile(r'{0}'.format(re.escape(query), re.IGNORECASE))
        results = Module.query.filter({ '$or': \
            [{'name': regex}, {'content': regex}]}).descending('created').paginate(page, count, error_out=False)
    else:
        results = Module.query.descending('created').paginate(page, count, error_out=False)
    ctx = {
        'modules': results,
        'search_query': query,
    }
    return render_template('modules/index.html', **ctx)

@bp.route('/newmodule', methods=['POST'])
@login_required
def new_module():
    mod = Module()
    mod.uuid = str(uuid4())
    mod.created = datetime.now()
    mod.author = session.get('user').uuid
    mod.name = request.form.get('name', 'Default')
    mod.description = request.form.get('description', '')
    mod.tags = request.form.get('tags', []).split()
    mod.save()
    return redirect(url_for('modules.index'))

@bp.route('/<uuid>/edit', methods=['GET', 'POST'])
@login_required
def edit_module(uuid=None):
    module = Module.get_by_uuid(uuid)
    form = ModuleForm(obj=module)
    if form.validate_on_submit():
        # validate
        if module:
            # update db
            data = form.data
            # update 
            module.update(**data)
            flash(messages.MODULE_UPDATED)
            return redirect(url_for('modules.index'))
    ctx = {
        'module': module,
        'form': form,
    }
    return render_template('modules/edit.html', **ctx)
    
