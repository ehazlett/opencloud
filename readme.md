OpenCloud : multi-account, multi-provider cloud manager
=======================================================
OpenCloud is a web application (written in Python using Flask) that manages various cloud platforms.

OpenCloud supports multiple organizations that can have multiple accounts with various providers.

View some [screenshots](http://bit.ly/Jbx00G).

Setup
-----
Prerequisites:

* Python 2.5+
* MongoDB
* Redis

To setup OpenCloud, clone the repo and use the following (this assumes you are using virtualenvs with `virtualenvwrapper`):

* `mkvirtualenv opencloud`
* `pip install -r requirements.txt`
* `python application.py --create-user`
* `python application.py`

You should now be able to view the application on `http://localhost:5000`

Configuration
--------------
OpenCloud allows multiple accounts for multiple providers (currently EC2 and Rackspace but growing).  To setup a provider, login as an admin and click the username dropdown in the upper right and select "accounts".  Click "New Account" and enter the provider credentials.  For `provider` use either `ec2` or `rackspace` at the moment.

These accounts will now show up in the dropdown list in the upper right when you login.  Provided you have entered proper credentials, you should be able to see your instances listed.