#!flask/bin/python
from flask import Flask, jsonify, Response, request, abort
from smsservice import SmsService
import json
from metadatastorage import MetadataStorage

app = Flask(__name__)

mds = MetadataStorage()

###
### Helper functions for return values
###

def expectNonemptyMapReturnAsJson(retval):
    if (not retval):
        return Response(status=500)
    else:
        return Response(json.dumps(retval), status=200, mimetype="application/json")

def allowEmptyMapReturnAsJson(retval, status=200):
    if (not retval):
        return Response(status=status)
    else:
        return Response(json.dumps(retval), status=status, mimetype="application/json")

def expectEmptyMapReturnErrorAsJson(retval, status=204):
     if (not bool(retval)):
         return Response(status=status)
     else:
         return Response(json.dumps(retval), status=500, mimetype="application/json")

 ###
 ### Media CRUD
 ###

@app.route('/media', methods = ['GET'])
def get_all_media():
     "Get a list of all the available media."
     return allowEmptyMapReturnAsJson([])

@app.route('/media/id/<id>', methods = ['GET'])
def get_media(id):
     "Get the media representation of identified asset"
     return Response(status=404)


@app.route('/media/', methods = ['POST'])
def create_new_media_entry_from_metadata():
     "Write the media representation an identified asset"
     returnValue = mds.createNewMediaEntraFromMetadata(request.json)
     return allowEmptyMapReturnAsJson(returnValue, status=201)

@app.route('/media/id/<id>', methods = ['POST'])
def post_media_to_id(id):
    "Write the media representation an identified asset"
    errorsMap = mds.post_media_to_id(id, request.mimetype, request.data)
    return expectEmptyMapReturnErrorAsJson(errorsMap, status=201)

@app.route('/media/id/<id>', methods = ['DELETE'])
def delete_media_and_meta(id):
    "Delete both media and metadata for an identified asset"
    return Response(status=404)


##
##  Meta CRUD
##
@app.route('/media/id/<id>/metatype/<metatype>', methods = ['GET'])
def get_meta_list(id, metatype):
    "Get list of metadata assets associated with a media asset"
    return Response(status=404)

@app.route('/media/id/<id>/metaid/<metaid>', methods = ['GET'])
def get_meta(id, metaid):
    "Get a particular metadata instance"
    return Response(status=404)

@app.route('/media/id/<id>/metatype/<metatype>', methods = ['POST'])
def post_new_meta(id, metatype):
    "Get list of metadata assets associated with a media asset"
    return Response(status=204)

@app.route('/media/id/<id>/metaid/<metaid>', methods = ['POST'])
def post_meta(id, metaid):
    "Post a particular metadata instance"
    return Response(status=404)

@app.route('/media/id/<id>/metaid/<metaid>', methods = ['DELETE'])
def delete_meta(id, metaid):
    "Get a particular metadata instance"
    return Response(status=404)

@app.route('/media/id/<id>/meta/<metatype>', methods = ['DELETE'])
def delete_meta_for_id(id, metatype):
    "Delete all metadata of a particular type for a specific media item"
    return Response(status=404)

 
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
