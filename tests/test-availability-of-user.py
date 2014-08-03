#!/usr/bin/python

import sys
import client
import errno
from get_test_auth import get_test_auth


# Pick a base url from the command line
base_url=str(sys.argv[1])

# Get auth parameters from environment variables
auth = get_test_auth()

if not auth:
    print ("Could not get auth")
    sys.exit(errno.ENOENT)
else:
    print ("Got auth = %r" % auth)

# Then set up a client against that server
cmc = client.ControlMetaClient(base_url, auth=auth)

# Do we have any users? If so everything is ok, otherwise fail.
users = cmc.get_users()
print ("All users (test-availability-of-user) = %r "% users)
if not users:
    print ("Users not found, bailing out")
    sys.exit(errno.ENOENT)
else:
    sys.exit(0)
