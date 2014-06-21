#!/usr/bin/python
from flask import Flask, jsonify, Response, request, abort
import json
from mediameta.mediametastorage import MediaAndMetaStorage
from database import db_session
from tasks.task_queue_storage import InMemoryTaskQueueStorage
import sys





# A class to hold a singleton instance. That instance
# holds the state of the application.

class State:

    def __init__(self):
        base_url="http://ctrl-meta.loltel.co"
        if (len(sys.argv) > 1):
            base_url=str(sys.argv[1])
        self.mms = MediaAndMetaStorage(base_url)
        self.tqs = InMemoryTaskQueueStorage()

    def clear(self):
        self.mms.clear();
        self.tqs.clear();


state = State()
state.clear()

##
## Helper functions to make it simpler to translate return values
## into response objects.
##

def expect_non_empty_map_return_as_json(retval, errorcode=404, status=200):
    if (not retval):
        return Response(status=errorcode)
    else:
        return Response(json.dumps(retval), status=status, mimetype="application/json")

def allow_empty_map_return_as_json(retval, status=200):
    if (not retval):
        return Response(status=status)
    else:
        return Response(json.dumps(retval), status=status, mimetype="application/json")

def expect_empty_map_return_error_as_json(retval, status=204, errorcode=404):
    if (not bool(retval)):
        return Response(status=status)
    else:
        # XXX The "use a map as a datastructure" antipattern, evaluate and refactor.
        if "HTTP_error_code" in retval:
            errorcode= retval["HTTP_error_code"]
        retvaldump=json.dumps(retval)
        return Response(retvaldump, status=errorcode, mimetype="application/json")

##
## Application lifecycle
##
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


##
##   Authentication
##
from functools import wraps
from flask import request, Response


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


    
###
###  Static pages
###

@app.route('/')
def hello_world():
    return "lol control meta!"


###
### Media CRUD
###


@app.route('/media', methods = ['GET'])
@requires_auth
def get_all_meta():
     "Get a list of all the available media's metadata."
     retval=state.mms.get_all_meta()
     return expect_non_empty_map_return_as_json(retval)

@app.route('/media/id/<id>', methods = ['GET'])
@requires_auth
def get_media(id):
     "Get the media representation of identified asset"
     mimetype, data = state.mms.get_media(id)
     if (not mimetype):
         return Response(status=404)
     else:
         return Response(data, mimetype=mimetype, status=200)

def get_requests_json(request):
    """Will return a pair of values (error, pval), where
     pval is the request parsed as python, and error is
     a Response object containing a parse error message
     that can be returned to the calling method. If no error
     is detected, the error value is None"""
    json_value  = request.json
    return None, json_value

## XXX This is bogus.   Here we should make media content, not
##     metadata!
@app.route('/media/', methods = ['POST'])
@requires_auth
def create_new_media_entry_from_upload():
     "Write the media representation an unidentified asset, returns the asset ID"
     retval = state.mms.create_new_media_entry(request.mimetype, request.data)
     return expect_non_empty_map_return_as_json(retval, status=201)

@app.route('/media/id/<id>', methods = ['POST'])
@requires_auth
def post_media_to_id(id):
    "Write the media representation an identified asset"
    errors = state.mms.post_media_to_id(id, request.mimetype, request.data)
    return expect_empty_map_return_error_as_json(errors, status=201)

@app.route('/media/id/<id>', methods = ['DELETE'])
@requires_auth
def delete_media_and_meta(id):
    "Delete both media and metadata for an identified asset"
    errors = state.mms.delete_media(id)
    return expect_empty_map_return_error_as_json(errors)


###
###  Meta CRUD
###


@app.route('/media/id/<id>/metatype/<metatype>', methods = ['GET'])
@requires_auth
def get_meta_list(id, metatype):
    "Get list of metadata assets associated with a media asset"
    retval = state.mms.get_meta_list(id, metatype)
    return expect_non_empty_map_return_as_json(retval)

@app.route('/media/id/<id>/metaid/<metaid>', methods = ['GET'])
@requires_auth
def get_meta(id, metaid):
    retval = state.mms.get_metadata_from_id(id, metaid)
    return expect_non_empty_map_return_as_json(retval)

@app.route('/media/id/<id>/metatype/<metatype>', methods = ['POST'])
@requires_auth
def post_new_meta(id, metatype):
    "Get list of metadata assets associated with a media asset"
    retval = state.mms.store_new_meta(id, metatype)
    return expect_non_empty_map_return_as_json(retval)

@app.route('/media/id/<id>/metaid/<metaid>', methods = ['POST'])
@requires_auth
def post_meta(id, metaid):
    "Post a particular metadata instance"
    retval = state.mms.store_meta(id, metaid)
    return expect_non_empty_map_return_as_json(retval)

@app.route('/media/id/<id>/metaid/<metaid>', methods = ['DELETE'])
@requires_auth
def delete_meta(id, metaid):
    "Delete a particular metadata instance"
    ## XXX This is f...ed up.
    retval = state.mms.delete_metaid(id, metaid)
    return expect_non_empty_map_return_as_json(retval)

###
###  Accessing the task queue
###


def tasklist_as_return_value(tasklist):
    retval = map(lambda x: x.as_map(), tasklist)
    return expect_non_empty_map_return_as_json(retval)

@app.route('/task/waiting', methods = ['GET'])
@requires_auth
def list_all_waiting_tasks():
    return tasklist_as_return_value(state.tqs.list_all_waiting_tasks())

@app.route('/task/running', methods = ['GET'])
@requires_auth
def get_in_progress_task_list():
    tasks = state.tqs.list_all_running_tasks()
    return tasklist_as_return_value(tasks)
        
@app.route('/task/type/<type>/done', methods = ['GET'])
@requires_auth
def get_done_task_list(type):
    return task_list_as_return_value(state.tqs.list_all_done_tasks())

@app.route('/task/waiting/type/<type>', methods = ['GET'])
@requires_auth
def list_waiting_task_of_type(type):
    return tasklist_as_return_value(state.tqs.list_all_waiting_tasks_of_type(type))
        
@app.route('/task/waiting/type/<type>/pick', methods = ['POST'])
@requires_auth
def pick_next_waiting_task(type):
    # XXX This code crashes, why?  
    # if not request.is_json():
    #     print "This isn't json"
    #     return expect_non_empty_map_return_as_json(
    #         {"Error description:" : "No agent description given when picking task" },
    #         errorcode=400)
    # XXX This will fail with a 500 error if the JSON is syntactically bogus
    #     We should test for that and fail gracefully instead
    agent_description=request.json
    if not agent_description:
        data = request.stream.read()
        return expect_non_empty_map_return_as_json(
            {"Error description:" : ("Agent description was not legal JSON syntax: '%s' "%(data)) },
            errorcode=400)
    task = state.tqs.pick_next_waiting_task_of_type(type, agent_description)
    return expect_non_empty_map_return_as_json(task)


@app.route('/task/id/<id>/done', methods = ['POST'])
@requires_auth
def declare_task_as_done(id):
    tqs=state.tqs
    retval = tqs.declare_as_done(id)
    return expect_empty_map_return_error_as_json(retval)
    
@app.route('/task/type/<type>', methods = ['POST'])
@requires_auth
def create_task(type):
    # Not sure about the semantics of this one.
    params=request.json
    if not params:
        params = request.stream.read()
        return expect_non_empty_map_return_as_json(
            {"Error description:" : ("Agent description was not legal JSON syntax: '%s' "%(data)) },
            errorcode=400)
    retval = state.tqs.create_task(type, params)
    return expect_non_empty_map_return_as_json(retval, status=201)

@app.route('/task/id/<taskid>', methods = ['DELETE'])
@requires_auth
def delete_task(taskid):
    retval = state.tqs.delete_task(taskid)
    return expect_empty_map_return_error_as_json(retval)

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
    state.clear()
