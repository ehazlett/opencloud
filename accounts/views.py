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
from accounts.models import Organization, Account, User
from accounts import forms
from decorators import admin_required
from uuid import uuid4
import utils
import messages
import re

bp = accounts_blueprint = Blueprint('accounts', __name__)
app = create_app()

@bp.route('/organizations/', methods=['GET'])
@login_required
@admin_required
def organizations():
    count = int(request.args.get('count', 15))
    page = int(request.args.get('page', 1))
    query = request.args.get('search', None)
    if query:
        regex = re.compile(r'{0}'.format(re.escape(query), re.IGNORECASE))
        results = Organization.query.filter({ '$or': \
            [{'name': regex}]}).paginate(page, count, error_out=False)
    else:
        results = Organization.query.ascending('name').paginate(page, count, error_out=False)
    ctx = {
        'organizations': results,
        'users': User.query.all(),
        'search_query': query,
    }
    return render_template('accounts/organizations.html', **ctx)

@bp.route('/organizations/create', methods=['POST'])
@login_required
@admin_required
def create_organization():
    org = Organization()
    org.name = request.form.get('name')
    org.owner = request.form.get('owner').lower()
    org.save()
    return redirect(url_for('accounts.organizations'))

@bp.route('/organizations/<uuid>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_organization(uuid=None):
    organization = Organization.get_by_uuid(uuid)
    form = forms.OrganizationForm(obj=organization)
    # HACK: WTForms doesn't do dynamic lookup on instantiation ; must set choices here otherwise
    # new users won't show up
    form.owner.choices = forms.get_user_choices()
    if form.validate_on_submit():
        # validate
        if organization:
            # update db
            data = form.data
            # update
            organization.update(**data)
            flash(messages.ORGANIZATION_UPDATED)
            return redirect(url_for('accounts.organizations'))
    ctx = {
        'organization': organization,
        'form': form,
    }
    return render_template('accounts/edit_organization.html', **ctx)

@bp.route('/organizations/<uuid>/delete')
@login_required
@admin_required
def delete_organizations(uuid=None):
    org = Organization.get_by_uuid(uuid)
    if org:
        org.remove()
    return redirect(url_for('accounts.organizations'))

# accounts
@bp.route('/', methods=['GET'])
@login_required
@admin_required
def accounts():
    count = int(request.args.get('count', 15))
    page = int(request.args.get('page', 1))
    query = request.args.get('search', None)
    if query:
        regex = re.compile(r'{0}'.format(re.escape(query), re.IGNORECASE))
        results = Account.query.filter({ '$or': \
            [{'name': regex}]}).paginate(page, count, error_out=False)
    else:
        results = Account.query.ascending('name').paginate(page, count, error_out=False)
    ctx = {
        'accounts': results,
        'organizations': Organization.query.ascending('name').all(),
        'search_query': query,
    }
    return render_template('accounts/accounts.html', **ctx)

@bp.route('/create', methods=['POST'])
@login_required
@admin_required
def create_account():
    act = Account()
    act.name = request.form.get('name')
    act.provider = request.form.get('provider')
    act.provider_id = request.form.get('provider_id')
    act.provider_key = request.form.get('provider_key')
    act.organization = request.form.get('organization').lower()
    act.save()
    return redirect(url_for('accounts.accounts'))

@bp.route('/<uuid>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_account(uuid=None):
    account = Account.get_by_uuid(uuid)
    if request.method == 'POST':
        if account:
            account.name = request.form.get('name')
            account.provider = request.form.get('provider')
            account.provider_id = request.form.get('provider_id')
            account.provider_key = request.form.get('provider_key')
            account.keypair = request.form.get('keypair', '')
            account.organization = request.form.get('organization', '')
            account.save()
            flash(messages.ACCOUNT_UPDATED)
            return redirect(url_for('accounts.accounts'))
    ctx = {
        'account': account,
        'organizations': Organization.query.ascending('name').all()
    }
    return render_template('accounts/edit_account.html', **ctx)

@bp.route('/<uuid>/delete')
@login_required
@admin_required
def delete_account(uuid=None):
    account = Account.get_by_uuid(uuid)
    if account:
        account.remove()
    return redirect(url_for('accounts.accounts'))

@bp.route('/<uuid>/defaultimages')
@login_required
@admin_required
def default_images(uuid=None):
    account = Account.get_by_uuid(uuid)
    ctx = {
        'account': account,
    }
    return render_template('accounts/_default_images.html', **ctx)

@bp.route('/<uuid>/updatedefaultimages', methods=['POST'])
@login_required
@admin_required
def update_default_images(uuid=None):
    account = Account.get_by_uuid(uuid)
    image_names = request.form.getlist('image_name')
    image_ids = request.form.getlist('image_id')
    image_regions = request.form.getlist('image_region')
    images = zip(image_names, image_ids, image_regions)
    default_images = []
    for img in images:
        d = {
            'name': img[0],
            'id': img[1],
            'region': img[2],
        }
        default_images.append(d)
    account.default_images = default_images
    account.save()
    flash('{0} {1}'.format(account.name, messages.DEFAULT_IMAGES_UPDATED), 'success')
    return redirect(url_for('accounts.accounts'))

# users
@bp.route('/users/', methods=['GET'])
@login_required
@admin_required
def users():
    count = int(request.args.get('count', 15))
    page = int(request.args.get('page', 1))
    query = request.args.get('search', None)
    if query:
        regex = re.compile(r'{0}'.format(re.escape(query), re.IGNORECASE))
        results = User.query.filter({ '$or': \
            [{'username': regex}, {'first_name': regex}, {'last_name': regex}, \
                {'email': regex}]}).ascending('username').paginate(page, count, error_out=False)
    else:
        results = User.query.ascending('username').paginate(page, count, error_out=False)
    ctx = {
        'users': results,
        'organizations': Organization.query.ascending('name').all(),
        'search_query': query,
    }
    return render_template('accounts/users.html', **ctx)

@bp.route('/users/create', methods=['POST'])
@login_required
@admin_required
def create_user():
    user = User()
    user.username = request.form.get('username', None)
    user.first_name = request.form.get('first_name', '')
    user.last_name = request.form.get('last_name', '')
    user.email = request.form.get('email', '')
    user.account = request.form.get('account', None)
    user.set_password(request.form.get('password', ''))
    user.save()
    return redirect(url_for('accounts.users'))

@bp.route('/users/<uuid>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(uuid=None):
    user = User.get_by_uuid(uuid)
    form = forms.UserEditForm(obj=user)
    # HACK: WTForms doesn't do dynamic lookup on instantiation ; must set choices here otherwise
    # new users won't show up
    form.organization.choices = forms.get_organization_choices()
    if form.validate_on_submit():
        # validate
        if user:
            # update db
            data = form.data
            # update
            user.update(**data)
            flash(messages.USER_UPDATED)
            return redirect(url_for('accounts.users'))
    ctx = {
        'user': user,
        'form': form,
    }
    return render_template('accounts/edit_user.html', **ctx)

@bp.route('/users/<uuid>/delete')
@login_required
@admin_required
def delete_user(uuid=None):
    user = User.get_by_uuid(uuid)
    if user:
        user.remove()
    return redirect(url_for('accounts.users'))

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    """
    User login

    """
    form = request.form
    if request.method == 'POST':
        organization = Organization.get_by_name(form.get('organization').lower())
        # validate
        user = User.get_by_username(form.get('username'), organization.uuid)
        if user:
            if utils.hash_password(form.get('password')) == user.password:
                login_user(user)
                session['user'] = user
                session['organization'] = organization
                current_app.logger.info('User {0} ({1}) login from {2}'.format(user.username, organization.name, \
                    request.remote_addr))
                return redirect(request.args.get("next") or url_for("index"))
        current_app.logger.warn('Invalid login for {0} ({1}) from {2}'.format(form.get('username'), organization.name, \
            request.remote_addr))
        flash(messages.INVALID_USERNAME_OR_PASSWORD, 'error')
    ctx = {
    }
    return render_template('accounts/login.html', **ctx)

@bp.route('/settings/', methods=['GET', 'POST'])
@login_required
def account_settings():
    """
    Account settings

    """
    user = session.get('user', None)
    form = forms.UserForm(obj=user)
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
    return render_template('accounts/edit_user.html', **ctx)

@bp.route('/generateapikey')
@login_required
def generate_api_key():
    return str(uuid4())

@bp.route('/setdefaultaccount/', methods=['POST'])
@login_required
def set_default_account():
    """
    Sets the default account for the session

    """
    session['default_account'] = request.form.get('account', None)
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

