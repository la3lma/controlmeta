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


# Pick a base url from the command line
base_url=str(sys.argv[1])

try:
    import httplib
except ImportError:
    import http.client as httplib
    
httplib.HTTPConnection.debuglevel = 1

logging.basicConfig(level=logging.DEBUG) # you need to initialize logging, 
                      # otherwise you will not see anything from requests

#

# Use the very secret admin password for testing
auth=HTTPBasicAuth('admin','secret')

# Then set up a client against that server
cmc = client.ControlMetaClient(base_url, auth=auth)

# Upload a piece of text
upload_result=cmc.upload_media("text/plain", "jalla")

# Retrieve the id and the url from the id
doc_id = upload_result.document_id
doc_url = upload_result.document_url
print "Text ID = ", doc_id
print "document url = ", doc_url

# Construct an URL based on the base URL (config problems)
# and use that to fetch the content

# Then upload an image from a file
filename='tests/images/lena1.jpeg'
file_upload_result = cmc.upload_media_from_file('image/jpeg', filename)
image_id = file_upload_result.document_id
image_url = file_upload_result.document_url

print "image ID = ", image_id
print "image document url = ", image_url

if not image_id :
    logging.debug("Could not get image ID")
    sys.exit(errno.ENOENT)

# XXX This fails !!
#     TODO:   Modify this thing into a failing unit test.
image_result=requests.get(image_url, auth=auth)

print "image result = ", image_result

