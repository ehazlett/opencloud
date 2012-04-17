OpenCloud : multi-account, multi-provider cloud manager
=======================================================
OpenCloud is a web application (written in Python using Flask) that manages various cloud platforms. 

Setup
-----
Prerequisites:

* Python 2.5+
* MongoDB

To setup OpenCloud, clone the repo and use the following (this assumes you are using virtualenvs with `virtualenvwrapper`):

* `mkvirtualenv opencloud`
* `pip install -r requirements.txt`
* `python application.py --create-user`
* `python application.py`

You should now be able to view the application on `http://localhost:5000`

Configuration
--------------
OpenCloud allows multiple accounts for multiple providers (currently EC2 and Rackspace but growing).  To setup your accounts, create a `config_local.json` file in the root of the application directory (you can copy `config.json` as a start).  OpenCloud uses the concept of "organizations" that allow for multiple accounts across providers.  Here is an example of multiple accounts (Amazon EC2 & Rackspace):

** Note: `ssh_key` must have new lines replaced with `\n`

```javascript
{
  "organizations": {
    "first account": {
      "api_keys": [
        "testapikey"
      ],
      "provider": "ec2",
      "provider_id": "ABCDEFGHIJKLMNOP",
      "provider_key": "1qaz2wsx3edc4rfv5tgb",
      "provider_data": {
        "keypair": "mykey"
      },
      "ssh_user": "root",
      "ssh_key": "-----BEGIN RSA PRIVATE KEY-----\nMLLEowIBBBKCAQEAxwQbvvT6M9xFMNDH7...\n-----END RSA PRIVATE KEY-----\n"
    },
    "second account": {
      "api_keys": [
        "testapikey"
      ],
      "provider": "rackspace",
      "provider_id": "myuseraccount",
      "provider_key": "1234567890abcdefghijklmnop",
      "provider_data": {},
      "ssh_user": "root",
      "ssh_key": "-----BEGIN RSA PRIVATE KEY-----\nMLLEowIBBBKCAQEAxwQbvvT6M9xFMNDH7...\n-----END RSA PRIVATE KEY-----\n"
    }
  }
}
```

These accounts will now show up in the dropdown list in the upper right when you login.  Provided you have entered proper credentials, you should be able to see your instances listed.