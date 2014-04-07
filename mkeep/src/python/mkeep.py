#!/usr/bin/python
from flask import Flask, jsonify, Response, request, abort
from smsservice import SmsService
import json
from mediametastorage import MediaAndMetaStorage
from taskqueuestorage import TaskQueueStorage

app = Flask(__name__)

### XXX This is a bug.  State is kept between instantiations
##      of the app instance.  That causes tests to break and it is
##      clearly the wrong thing to do. Investigate and fix.

mms = MediaAndMetaStorage()
tqs = TaskQueueStorage()


###
### Helper functions for return values
###

def expect_non_empty_map_return_as_json(retval, errorcode=500, status=200):
    if (not retval):
        return Response(status=errorcode)
    else:
        return Response(json.dumps(retval), status=status, mimetype="application/json")

def allow_empty_map_return_as_json(retval, status=200):
    if (not retval):
        return Response(status=status)
    else:
        return Response(json.dumps(retval), status=status, mimetype="application/json")

def expect_empty_map_return_error_as_json(retval, status=204, errorcode=500):
    if (not bool(retval)):
        return Response(status=status)
    else:
        # XXX The "use a map as a datastructure" antipattern, evaluate and refactor.
        if "HTTP_error_code" in retval:
            errorcode= retval["HTTP_error_code"]
        retvaldump=json.dumps(retval)
        return Response(retvaldump, status=errorcode, mimetype="application/json")

###
### Media CRUD
###

@app.route('/media', methods = ['GET'])
def get_all_meta():
     "Get a list of all the available media's metadata."
     retval=mms.get_all_meta()
     return expect_non_empty_map_return_as_json(retval, errorcode=404)

@app.route('/media/id/<id>', methods = ['GET'])
def get_media(id):
     "Get the media representation of identified asset"
     mimetype, data = mms.get_media(id)
     if (not mimetype):
         return Response(status=404)
     else:
         return Response(data, mimetype=mimetype, status=200)

@app.route('/media/', methods = ['POST'])
def create_new_media_entry_from_metadata():
     "Write the media representation an identified asset"
     retval = mms.create_new_media_entry_from_metadata(request.json)
     return allow_empty_map_return_as_json(retval, status=201)

@app.route('/media/id/<id>', methods = ['POST'])
def post_media_to_id(id):
    "Write the media representation an identified asset"
    errors = mms.post_media_to_id(id, request.mimetype, request.data)
    return expect_empty_map_return_error_as_json(errors, status=201)

@app.route('/media/id/<id>', methods = ['DELETE'])
def delete_media_and_meta(id):
    "Delete both media and metadata for an identified asset"
    errors = mms.delete_media(id)
    return expect_empty_map_return_error_as_json(errors, errorcode=404, status=204)


###
###  Meta CRUD
###
@app.route('/media/id/<id>/metatype/<metatype>', methods = ['GET'])
def get_meta_list(id, metatype):
    "Get list of metadata assets associated with a media asset"
    retval = mms.get_meta_list(id, metatype)
    return expect_non_empty_map_return_as_json(retval, status=200, errorcode=404)

@app.route('/media/id/<id>/metaid/<metaid>', methods = ['GET'])
def get_meta(id, metaid):
    retval = mms.get_metadata_from_id(id, metaid)
    return expect_non_empty_map_return_as_json(retval, status=200, errorcode=404)

@app.route('/media/id/<id>/metatype/<metatype>', methods = ['POST'])
def post_new_meta(id, metatype):
    "Get list of metadata assets associated with a media asset"
    retval = mms.store_new_meta(id, metatype)
    return expect_non_empty_map_return_as_json(retval, status=200, errorcode=404)

@app.route('/media/id/<id>/metaid/<metaid>', methods = ['POST'])
def post_meta(id, metaid):
    "Post a particular metadata instance"
    retval = mms.store_meta(id, metaid)
    return expect_non_empty_map_return_as_json(retval, status=200, errorcode=404)

@app.route('/media/id/<id>/metaid/<metaid>', methods = ['DELETE'])
def delete_meta(id, metaid):
    "Delete a particular metadata instance"
    retval = mms.delete_metaid(id, metaid)
    return expect_non_empty_map_return_as_json(retval, errorcode=404, status=200)

###
###  Accessing the task queue
###


@app.route('/task/waiting', methods = ['GET'])
def list_all_waiting_tasks():
    retval = tqs.list_all_waiting_tasks()
    return expect_non_empty_map_return_as_json(retval, errorcode=404, status=200)

@app.route('/task/waiting/type/<type>', methods = ['GET'])
def list_waiting_task_of_type(type):
    retval = tqs.list_all_waiting_tasks_of_type(type)
    return expect_non_empty_map_return_as_json(retval, errorcode=404, status=200)

        
@app.route('/task/waiting/type/<type>/pick', methods = ['POST'])
def pick_next_waiting_task(type):
    # XXX This thing should fail if there is no runner field in the
    #     post statement
    retval = tqs.pick_next_waiting_task_of_type(type, "XXXX Dummy runner")
    return expect_non_empty_map_return_as_json(retval, errorcode=404, status=200)

@app.route('/task/type/<type>/in-progress', methods = ['GET'])
def get_in_progress_task_list(type):
    retval = tqs.list_all_running_tasks()
    return expect_non_empty_map_return_as_json(retval, errorcode=404, status=200)
        
@app.route('/task/type/<type>/done', methods = ['GET'])
def get_done_task_list(type):
    retval = tqs.list_all_done_tasks()
    return expect_non_empty_map_return_as_json(retval, errorcode=404, status=200)

@app.route('/task/type/<id>/done', methods = ['POST'])
def declare_task_as_done(id):
    retval = tqs.declare_as_done()
    return expect_non_empty_map_return_as_json(retval, errorcode=404, status=200)
    
@app.route('/task/type/<type>', methods = ['POST'])
def create_task(type):
    retval = tqs.create_task(type)
    return expect_non_empty_map_return_as_json(retval, errorcode=404, status=201)

@app.route('/task/id/<taskid>', methods = ['DELETE'])
def delete_task(taskid):
    retval = tqs.delete_task(taskid)
    return expect_empty_map_return_error_as_json(retval, status=200)

if __name__ == '__main__':
    app.run(debug = True)

