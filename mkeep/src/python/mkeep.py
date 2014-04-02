#!/bin/python
from flask import Flask, jsonify, Response, request, abort
from smsservice import SmsService
import json
from mediametastorage import MediaAndMetaStorage
from taskqueuestorage import TaskQueueStorage

app = Flask(__name__)

mms = MediaAndMetaStorage()
tqs = TaskQueueStorage()

###
### Helper functions for return values
###

def expectNonemptyMapReturnAsJson(retval, errorcode=500, status=200):
    if (not retval):
        return Response(status=errorcode)
    else:
        print errorcode
        return Response(json.dumps(retval), status=status, mimetype="application/json")

def allowEmptyMapReturnAsJson(retval, status=200):
    if (not retval):
        return Response(status=status)
    else:
        return Response(json.dumps(retval), status=status, mimetype="application/json")

def expectEmptyMapReturnErrorAsJson(retval, status=204, errorcode=500):
    if (not bool(retval)):
        return Response(status=status)
    else:
        return Response(json.dumps(retval), status=errorcode, mimetype="application/json")

###
### Media CRUD
###

@app.route('/media', methods = ['GET'])
def get_all_meta():
     "Get a list of all the available media's metadata."
     return expectNonemptyMapReturnAsJson(mms.get_all_meta(), errorcode=404)

@app.route('/media/id/<id>', methods = ['GET'])
def get_media(id):
     "Get the media representation of identified asset"
     mimetype, data = mms.get_media(id)
     if (not mimetype):
         return Response(status=404)
     else:
         print "oranbge"
         return Response(data, mimetype=mimetype, status=200)

@app.route('/media/', methods = ['POST'])
def create_new_media_entry_from_metadata():
     "Write the media representation an identified asset"
     returnValue = mms.create_new_media_entry_from_metadata(request.json)
     return allowEmptyMapReturnAsJson(returnValue, status=201)

@app.route('/media/id/<id>', methods = ['POST'])
def post_media_to_id(id):
    "Write the media representation an identified asset"
    errorsMap = mms.post_media_to_id(id, request.mimetype, request.data)
    return expectEmptyMapReturnErrorAsJson(errorsMap, status=201)

@app.route('/media/id/<id>', methods = ['DELETE'])
def delete_media_and_meta(id):
    "Delete both media and metadata for an identified asset"
    errors = mms.delete_media(id)
    return expectEmptyMapReturnErrorAsJson(errors, status=204)


###
###  Meta CRUD
###
@app.route('/media/id/<id>/metatype/<metatype>', methods = ['GET'])
def get_meta_list(id, metatype):
    "Get list of metadata assets associated with a media asset"
    metalist = mms.get_meta_list(id, metatype)
    return expectNonemptyMapReturnAsJson(metalist, status=200, errorcode=404)


@app.route('/media/id/<id>/metaid/<metaid>', methods = ['GET'])
def get_meta(id, metaid):
    metadata = mms.get_metadata_from_id(id, metaid)
    return expectNonemptyMapReturnAsJson(metadata, status=200, errorcode=404)


@app.route('/media/id/<id>/metatype/<metatype>', methods = ['POST'])
def post_new_meta(id, metatype):
    "Get list of metadata assets associated with a media asset"
    postresult = mms.store_new_meta(id, metatype)
    return expectNonemptyMapReturnAsJson(postresult, status=200, errorcode=404)


@app.route('/media/id/<id>/metaid/<metaid>', methods = ['POST'])
def post_meta(id, metaid):
    "Post a particular metadata instance"
    postresult = mms.store_meta(id, metaid)
    return expectNonemptyMapReturnAsJson(postresult, status=200, errorcode=404)

@app.route('/media/id/<id>/metaid/<metaid>', methods = ['DELETE'])
def delete_meta(id, metaid):
    "Delete a particular metadata instance"
    retval = mms.delete_metaid(id, metaid)
    return expectNonemptyMapReturnAsJson(retval, errorcode=404, status=200)

###
###  Accessing the task queue
###


@app.route('/task/waiting', methods = ['GET'])
def list_all_waiting_tasks():
    return Response(status=404)

@app.route('/task/waiting/type/<type>', methods = ['GET'])
def list_waiting_task_of_type(type):
    return Response(status=404)

@app.route('/task/waiting/type/<type>/next', methods = ['GET'])
def get_next_waiting_task(type):
    return Response(status=404)
        
@app.route('/task/waiting/type/<type>/next', methods = ['POST'])
def pick_next_waiting_task(type):
    return Response(status=404)

@app.route('/task/type/<type>/in-progress', methods = ['GET'])
def get_in_progress_task_list(type):
    return Response(status=404)
        
@app.route('/task/type/<type>/done', methods = ['GET'])
def get_done_task_list(type):
    return Response(status=404)

@app.route('/task/type/<id>/done', methods = ['POST'])
def declare_task_as_done(id):
    return Response(status=404)

@app.route('/task/type/<type>', methods = ['POST'])
def create_new_task(type):
    return Response(status=204)


if __name__ == '__main__':
    app.run(debug = True)
