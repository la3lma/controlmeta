#!/usr/bin/python

import sys
import client
import logging
import errno
from get_test_auth import get_test_auth

# Pick a base url from the command line
base_url=str(sys.argv[1])

# you need to initialize logging, 
# otherwise you will not see anything from requests
logging.basicConfig(level=logging.DEBUG) 

# Get auth parameters from environment variables
auth = get_test_auth()

if not auth:
    logging.debug("Could not get auth")
    sys.exit(errno.ENOENT)

# Then set up a client against that server
cmc = client.ControlMetaClient(base_url, auth=auth)

# Do we have any users? If so everything is ok, otherwise fail.
users = cmc.get_users()
logging.debug("All users = %r "% users)
if not users:
    sys.exit(errno.ENOENT)
