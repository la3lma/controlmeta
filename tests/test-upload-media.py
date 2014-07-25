#!/usr/bin/python

import sys
import client
import logging
import requests
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
import logging
logging.basicConfig(level=logging.DEBUG)
import errno, sys
from get_test_auth import get_test_auth


# Pick a base url from the command line
base_url=str(sys.argv[1])

try:
    import httplib
except ImportError:
    import http.client as httplib
    
httplib.HTTPConnection.debuglevel = 1

# you need to initialize logging, 
# otherwise you will not see anything from requests
logging.basicConfig(level=logging.DEBUG) 


# Get auth parameters from environment variables
auth = get_test_auth()

# Then set up a client against that server
cmc = client.ControlMetaClient(base_url, auth=auth)

# Then get the usedata for all the users
def print_all_users(location):
    users = cmc.get_users()
    print "All users @%r = %r "% (location, users)
    if not users:
        raise Exception("Could not find any users")

print_all_users("beginning")

# Upload a piece of text
upload_result=cmc.upload_media("text/plain", "jalla")

# Retrieve the id and the url from the id
doc_id = upload_result.document_id
doc_url = upload_result.document_url

# Construct an URL based on the base URL (config problems)
# and use that to fetch the content

# Then upload an image from a file
filepath='tests/images/lena1.jpeg'
file_upload_result = cmc.upload_media_from_file('image/jpeg', filepath)
image_id = file_upload_result.document_id
image_url = file_upload_result.document_url


if not image_id :
    logging.debug("Could not get image ID")
    sys.exit(errno.ENOENT)

# XXX This fails !!
#     TODO:   Modify this thing into a failing unit test.
image_result=requests.get(image_url, auth=auth)


print_all_users("before_upload")

with open(filepath, 'r') as content_file:
    content = content_file.read()

if content != image_result.content :
    logging.debug("content != image_result.content, so we fail")
    sys.exit(errno.ENOENT)


