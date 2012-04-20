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
import application
import unittest
from test_helpers import create_user, delete_user

class TestDashboard(unittest.TestCase):
    def setUp(self):
        self.app = application.app.test_client()
        self.test_user_username = 'testuser'
        self.test_user_password = '1q2w3e'
        # disable csrf for flask-wtf posts
        application.app.config['CSRF_ENABLED'] = False
        # create test user
        create_user(self.test_user_username, '', self.test_user_password)
        # login user
        self.login()

    def tearDown(self):
        self.app.get('/accounts/logout/')
        delete_user(self.test_user_username)

    def login(self):
        rv = self.app.post('/accounts/login/', data={
            'username': self.test_user_username,
            'password': self.test_user_password,
        }, follow_redirects=True)
        return rv