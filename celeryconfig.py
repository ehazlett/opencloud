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
import config

BROKER_URL = "redis://{0}:{1}/{2}".format(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB)
CELERY_RESULT_BACKEND = "redis"
CELERY_REDIS_HOST = config.REDIS_HOST
CELERY_REDIS_PORT = config.REDIS_PORT
CELERY_REDIS_DB = config.REDIS_DB
CELERY_IMPORTS = (,)
CELERY_TASK_RESULT_EXPIRES = 86400