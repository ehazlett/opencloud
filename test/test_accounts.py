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

class TestAccounts(unittest.TestCase):
    def setUp(self):
        self.app = application.app.test_client()

    def tearDown(self):
        pass

    def test_login(self):
        rv = self.app.get('/accounts/login/')
        self.assertEqual(rv.status_code, 200)
