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
from flaskext.login import login_user, logout_user, login_required
from config import create_app
from accounts.models import User
from accounts.forms import LoginForm, AccountForm, AccountEditForm
from decorators import admin_required
import utils
import messages
import re

bp = accounts_blueprint = Blueprint('accounts', __name__)
app = create_app()

@bp.route('/', methods=['GET'])
@login_required
@admin_required
def index():
    count = int(request.args.get('count', 15))
    page = int(request.args.get('page', 1))
    query = request.args.get('search', None)
    if query:
        regex = re.compile(r'{0}'.format(re.escape(query), re.IGNORECASE))
        results = User.query.filter({ '$or': \
            [{'username': regex}, {'first_name': regex}, {'last_name': regex}, {'email': regex}]}).ascending('username').paginate(page, count, error_out=False)
    else:
        results = User.query.ascending('username').paginate(page, count, error_out=False)
    ctx = {
        'users': results,
        'search_query': query,
    }
    return render_template('accounts/index.html', **ctx)

@bp.route('/create', methods=['POST'])
@login_required
@admin_required
def create():
    user = User()
    user.username = request.form.get('username', None)
    user.first_name = request.form.get('first_name', '')
    user.last_name = request.form.get('last_name', '')
    user.email = request.form.get('email', '')
    user.set_password(request.form.get('password', ''))
    user.save()
    return redirect(url_for('accounts.index'))

@bp.route('/<uuid>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(uuid=None):
    user = User.get_by_uuid(uuid)
    form = AccountEditForm(obj=user)
    if form.validate_on_submit():
        # validate
        if user:
            # update db
            data = form.data
            # update
            user.update(**data)
            flash(messages.USER_UPDATED)
            return redirect(url_for('accounts.index'))
    ctx = {
        'user': user,
        'form': form,
    }
    return render_template('accounts/settings.html', **ctx)

@bp.route('/<username>/delete')
@login_required
@admin_required
def delete_account(username=None):
    user = User.get_by_username(username)
    if user:
        user.remove()
    return redirect(url_for('accounts.index'))

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Account login

    """
    form = LoginForm()
    if form.validate_on_submit():
        # validate
        user = User.get_by_username(form.username.data)
        if user:
            if utils.hash_password(form.password.data) == user.password:
                login_user(user)
                session['user'] = user
                current_app.logger.info('User {0} login from {1}'.format(user.username, request.remote_addr))
                return redirect(request.args.get("next") or url_for("index"))
        current_app.logger.warn('Invalid login for {0} from {1}'.format(form.username.data, request.remote_addr))
        flash(messages.INVALID_USERNAME_OR_PASSWORD, 'error')
    ctx = {
        'form': form,
    }
    return render_template('accounts/login.html', **ctx)

@bp.route('/settings/', methods=['GET', 'POST'])
@login_required
def settings():
    """
    Account settings

    """
    user = session.get('user', None)
    form = AccountForm(obj=user)
    if form.validate_on_submit():
        # validate
        if user:
            # update db
            data = form.data
            # update
            user.update(**data)
            # update the session user
            session['user'] = User.get_by_uuid(user.uuid)
            flash(messages.ACCOUNT_UPDATED)
    ctx = {
        'account': session.get('user', None),
        'form': form,
    }
    return render_template('accounts/settings.html', **ctx)

@bp.route('/setdefaultorg/', methods=['POST'])
@login_required
def set_default_org():
    """
    Sets the default organization for the session

    """
    session['default_organization'] = request.form.get('org', None)
    return ''

@bp.route('/logout/', methods=['GET'])
@login_required
def logout():
    """
    Logs out current user

    """
    current_app.logger.info('{0} logout from {1}'.format(session['user'].username, request.remote_addr))
    session.pop('user')
    logout_user()
    flash(messages.LOGGED_OUT)
    return redirect(url_for('index'))

