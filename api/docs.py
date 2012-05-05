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
from flaskext.babel import gettext

def nodes():
    """
    API documentation for `api.views.nodes`
    
    """
    data = {
        'uri': '/nodes/<organization>/<provider>/<region>/',
        'info': gettext('Returns nodes in the region of the provider for the specified organization'),
        'parameters': {
            'id': gettext('Node ID to use as a filter'),
        }
    }
    return data