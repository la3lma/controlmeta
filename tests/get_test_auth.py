#!/usr/bin/python
from requests.auth import HTTPBasicAuth
import os


def get_test_auth():
    username = None
    password = None
    
    if 'USERNAME' in os.environ:
        username = os.environ["USERNAME"]
    else:
        raise Exception("No environment variable USERNAME found")
        
    if 'PASSWORD' in os.environ:
        password = os.environ["PASSWORD"]
    else:
        raise Exception("No environment variable PASSWORD found")
            
    # Use the very secret admin password for testing
    auth = HTTPBasicAuth(username, password)

    print "Client will authenticate using %r/%r"%(username, password)

    return auth

