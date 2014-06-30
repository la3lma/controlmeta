#!/bin/python

import sys
import os
import client
import logging
import requests
from imagemagic_identify_output_parser import parse_image_file
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
import logging
logging.basicConfig(level=logging.DEBUG)
import errno, sys


# This is a simple test of a full roundtrip where we
#  o Set up connetions to the server
#  o Upload an image
#  o Create a task-entry  for processing it in some way.
#  o Run a processor that will fetch the image and
#    process it, producing some metadata that will then be
#    uploaded
#  o Finally we list the metadata for the image.


##
##  Boilerplate to set up a client that can talk to the server
##
# Pick a base url from the command line
base_url=str(sys.argv[1])

try:
    import httplib
except ImportError:
    import http.client as httplib
    
httplib.HTTPConnection.debuglevel = 1

logging.basicConfig(level=logging.DEBUG) # you need to initialize logging, 
                      # otherwise you will not see anything from requests


# Use the very secret admin password for testing
auth=HTTPBasicAuth('admin','secret')

# Then set up a client against that server
cmc = client.ControlMetaClient(base_url, auth=auth)

##
## Then upload an image from a file
##
filepath='tests/images/lena1.jpeg'
file_upload_result = cmc.upload_media_from_file('image/jpeg', filepath)
image_id = file_upload_result.document_id
image_url = file_upload_result.document_url


###
### This set of task initiations should be triggered
### automatically by the upload.  A separate agent should 
### do this, the central storage service should be completely
### ignorant.
###

##
## The create a task based on this image to extract
## "basic info" from the image, whatever that turns out to be.
##

parameters={'image_id':str(image_id)}
data = cmc.upload_task("extract_image_basics", parameters)
data = cmc.upload_task("find_faces", parameters)


###
### This function should be triggered by the creation of
### an "extract_image_basics" task.   It should be an agent
### running somewhere, in some very restricted environment
### where it can create tempfiles, but not very much else
###


## Then pick the first task that matches the "extract_image_basics" pattern
## using imagemagick
##

task = cmc.pick_task("extract_image_basics", "agent_009")
task_image_id =  task.parameters['image_id']
(tempfile_name, mediatype) = cmc.get_media_to_tempfile(task_image_id)
basic_info = parse_image_file(tempfile_name)
os.remove(tempfile_name)

cmc.upload_metadata_for_media(task_image_id, "basic_image_infos", basic_info)


###
### This function should be triggered by the creation of
### an "find_faces" task.   It should be an agent
### running somewhere, in some very restricted environment
### where it can create tempfiles, but not very much else
###


##
## Then pick the first task that matches the "extract_image_basics" pattern
## and extract faces using haar transforms from opencv
##

import cv2




###
###  Then we do the thing with  recognizing faces in a picture.
###

haar_cascade_home='/usr/local/Cellar/opencv/2.4.6.1/share/OpenCV/haarcascades/'

def hc(p):
    return haar_cascade_home + p

def detect(path):
    img = cv2.imread(path)
    cascade = cv2.CascadeClassifier(hc("haarcascade_frontalface_alt.xml"))
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    return rects, img

def box(rects, img):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
    cv2.imwrite('detected.jpg', img);


# Get the image and drop it in a file
task = cmc.pick_task("find_faces", "agent_009")
task_image_id =  task.parameters['image_id']


(tempfile_name, mediatype) = cmc.get_media_to_tempfile(task_image_id)

# Extract all the faces
faces, img = detect(tempfile_name)
os.remove(tempfile_name)

# If faces were found, add them as individual metadata-pices
for x1, y1, x2, y2 in faces:

    # Extract the face
    face  = img[y1:y2, x1:x2]
    cv2.imwrite('detected_face.jpg', face)

    # Upload it
    file_upload_result = cmc.upload_media_from_file('image/jpeg', 'detected_face.jpg')
    image_id = file_upload_result.document_id
    image_url = file_upload_result.document_url


    # Upload metadata about where the image is located
    metadata = {"location_in_original": {"x1":str(x1), "y1":str(y1), "x2":str(x2), "y2":str(y2)},
                "media_id_of_subimage": str(image_id)}
    cmc.upload_metadata_for_media(task_image_id, "face", metadata)


    # XXX Missing
    #     Create a new image containing the face and upload it. It should be linked
    #     to the original image in some way, or perhaps to the metadata in some other
    #     strange way. In any case, when the original image dissapears, this copy should
    #     also get zapped.


## 
## XXX  Test that the metadata about the location of the faces  was actually
##      written  to storage.


