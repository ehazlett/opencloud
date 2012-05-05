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
from flask import url_for, g
from flaskext.babel import gettext
from functools import wraps

def load_api_url_prefix(f):
    """
    Loads the API url prefix into the `flask.g` object.  We use a decorator to bypass the "working out of context" flask 
    error you get when using url_for out of a request context.
    
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        g.api_url_prefix = url_for('api.index')
        return f(*args, **kwargs)
    return decorated

@load_api_url_prefix
def nodes():
    """
    API documentation for `api.views.nodes`

    """
    data = {
        'uri': '{0}/<organization>/nodes/<account>/<provider>/<region>/'.format(g.api_url_prefix),
        'info': gettext('Returns nodes in the region of the provider for the account in the specified organization'),
        'parameters': {
            'id': gettext('Node ID to use as a filter'),
        }
    }
    return data