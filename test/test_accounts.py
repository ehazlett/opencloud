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
from accounts.models import username_validator, User
from test_helpers import create_user, delete_user

class TestAccounts(unittest.TestCase):
    def setUp(self):
        self.app = application.app.test_client()
        self.test_user_username = 'testsampleuser'
        self.test_user_email = 'sample@opencloud'
        self.test_user_password = 'test123'
        # disable csrf for flask-wtf posts
        application.app.config['CSRF_ENABLED'] = False

    def tearDown(self):
        pass

    def test_login_status_200(self):
        rv = self.app.get('/accounts/login/')
        self.assertEqual(rv.status_code, 200)
        
    def test_username_validator_valid_username(self):
        username = 'sampleuser'
        self.assertTrue(username_validator(username))
        
    def test_username_validator_invalid_username(self):
        username = 's@#mpl3'
        self.assertFalse(username_validator(username))
        
    def test_create_delete_user(self):
        username = self.test_user_username
        email = self.test_user_email
        password = self.test_user_password
        self.assertTrue(create_user(username, email, password))
        self.assertTrue(User.get_by_username(self.test_user_username))
        self.assertTrue(delete_user(username))
