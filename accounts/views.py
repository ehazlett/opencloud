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
from accounts.forms import LoginForm, AccountForm
import utils
import messages

bp = accounts_blueprint = Blueprint('accounts', __name__)
app = create_app()

@bp.context_processor
def load_user():
    return {'user': session.get('user', None)}

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
                return redirect(request.args.get("next") or url_for("index"))
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
    session.pop('user')
    logout_user()
    flash(messages.LOGGED_OUT)
    return redirect(url_for('index'))

