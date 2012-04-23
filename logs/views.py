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
from logs.models import Log
import re

bp = logs_blueprint = Blueprint('logs', __name__)

@bp.route('/')
@login_required
def index():
    count = int(request.args.get('count', 15))
    page = int(request.args.get('page', 1))
    query = request.args.get('search', None)
    if query:
        regex = re.compile(r'{0}'.format(re.escape(query), re.IGNORECASE))
        results = Log.query.filter({ '$or': \
            [{'name': regex}, {'message': regex}]}).descending('date').paginate(page, count, error_out=False)
    else:
        results = Log.query.descending('date').paginate(page, count, error_out=False)
    ctx = {
        'logs': results,
        'search_query': query,
    }
    return render_template('logs/index.html', **ctx)

@bp.route('/clear/')
@login_required
def clear():
    Log.clear()
    return redirect(url_for('logs.index'))
