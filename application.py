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
import sys
from getpass import getpass
from flask import Flask
from flask import jsonify
from flask import request
from flask import session
from flask import redirect, render_template, url_for
from flask import g
from flaskext.login import login_required
from flaskext.login import LoginManager
from flaskext.babel import Babel
import config
from raven.contrib.flask import Sentry
#from api.views import api_blueprint
from accounts.views import accounts_blueprint
from dashboard.views import dashboard_blueprint
from accounts.models import User

sentry = Sentry(config.SENTRY_DSN)

app = config.create_app()
#app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(accounts_blueprint, url_prefix='/accounts')
app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
babel = Babel(app)
login_manager = LoginManager()
login_manager.setup_app(app)

@login_manager.user_loader
def user_loader(user_id):
    return User.get_by_uuid(user_id)

@login_manager.unauthorized_handler
def login_unauthorized():
    return redirect(url_for('accounts.login'))

@app.route('/')
@login_required
def index():
    return redirect(url_for('dashboard.index'))

# ----- management commands -----
def create_user():
    try:
        username = raw_input('Username: ').strip()
        email = raw_input('Email: ').strip()
        while True:
            password = getpass('Password: ')
            password_confirm = getpass(' (confirm): ')
            if password_confirm == password:
                break
            else:
                print('Passwords do not match... Try again...')
        u = User(username=username)
        u.email = email
        u.set_password(password)
        u.save()
        print('User created/updated successfully...')
    except KeyboardInterrupt:
        pass

if __name__=='__main__':
    from optparse import OptionParser
    op = OptionParser()
    op.add_option('--host', dest='host', action='store', default='127.0.0.1', help='Hostname/IP on which to listen')
    op.add_option('--create-user', dest='create_user', action='store_true', default=False, help='Create/update user')
    opts, args = op.parse_args()

    if opts.create_user:
        create_user()
        sys.exit(0)
        
    app.run(host=opts.host, debug=True)
