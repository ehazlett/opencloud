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
import utils
import unittest
import config

class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_hash_password(self):
        config.SECRET_KEY = 'secret'
        passwd = 'mysecretpass'
        hashed = '3cd0adf8cb8bb218f8ad97fd1b1f39c240c95e59bf94fabe932048fe11b53bbc'
        self.assertEqual(utils.hash_password(passwd), hashed)