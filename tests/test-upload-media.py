#!/usr/bin/python

import sys
import client
import requests
    
# Pick a base url from the command line
base_url=str(sys.argv[1])


# Then set up a client against that server
cmc = client.ControlMetaClient(base_url)

# Upload a piece of text
upload_result=cmc.upload_media("text/plain", "jalla")

# Retrieve the id and the url from the id
doc_id = upload_result.document_id
doc_url = upload_result.document_url
print "Text ID = ", doc_id
print "document url = ", doc_url

# Construct an URL based on the base URL (config problems)
# and use that to fetch the content

# Then upload an image from a file XXX Does not work!
filename='imageprocessors/sample-images/lena1.jpeg'
file_upload_result = cmc.upload_media_from_file('image/jpeg', filename)
image_id = file_upload_result.document_id
image_url = file_upload_result.document_url
print "image ID = ", image_id
print "image document url = ", image_url

image_result=requests.get(image_url)

print "image result = ", image_result

