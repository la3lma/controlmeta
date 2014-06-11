from flask import  jsonify, Response, request, abort
import json
import sys

from ctlm import app
from database import Base, db_session, init_db, commit_db
from mediameta.model import RDBMSMediaAndMetaStorage, ModelException
from task.model import RDBQueueStorage

import logging
logging.basicConfig(level=logging.DEBUG)

# A class to hold a singleton instance. That instance                                  
# holds the state of the application.                                                  
# XXX This is a kludge, for sure.

class State:

    def __init__(self):
        base_url="http://ctlmeta.loltel.co"
        if (len(sys.argv) > 1):
            base_url=str(sys.argv[1])
        self.mms = RDBMSMediaAndMetaStorage(base_url)
        self.tqs = RDBQueueStorage()

        # This _should_ declare the database tables
        # XXX This only makes sense during test, it would
        #     completely mess things up in prod.
        #   Actually, it only makes sense during unit tests, and perhaps
        #   not even  then.
        #   init_db()

state = State()


##
## Helper functions to make it simpler to translate return values
## into response objects.
##

def expect_non_empty_map_return_as_json(retval, errorcode=404, status=200):
    if (not retval):
        return Response(status=errorcode)
    else:
        commit_db()
        return Response(json.dumps(retval), status=status, mimetype="application/json")

def allow_empty_map_return_as_json(retval, status=200):
    commit_db()
    if (not retval):
        return Response(status=status)
    else:
        return Response(json.dumps(retval), status=status, mimetype="application/json")

def expect_empty_map_return_error_as_json(retval, status=204, errorcode=404):
    if (not bool(retval)):
        commit_db()
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

        if not auth:
            return authenticate()

        elif  not check_auth(auth.username, auth.password):
            return authenticate()

        else:
            return f(*args, **kwargs)
    return decorated

def catches_model_exception(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ModelException as e:
            # XXX When this has been proven to work, create a wrapper and put all
            #     functions inside that wrapper.
            print "Caught Model Exception: " , e
            return Response(
                json.dumps(e.message),
                status=e.http_returnvalue,
                mimetype="application/json")
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
def get_all_media():
     "Get a list of all the available media's metadata."
     retval=state.mms.get_all_media()
     rv =  expect_non_empty_map_return_as_json(retval)
     return rv

@app.route('/media/id/<id>', methods = ['GET'])
@requires_auth
def get_media(id):
     "Get the media representation of identified asset"
     mimetype, data = state.mms.get_media(id)
     if (not mimetype):
         return Response(status=404)
     else:
         return Response(data, mimetype=mimetype, status=200)

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
@catches_model_exception
def get_meta_list_from_id_and_metaid(id, metatype):
    "Get list of metadata assets associated with a media asset"
    retval = state.mms.get_metadata_from_id_and_metatype(id, metatype)
    return expect_non_empty_map_return_as_json(retval)

@app.route('/media/id/<id>/metaid/<metaid>', methods = ['GET'])
@requires_auth
@catches_model_exception
def get_metadata_from_id_and_metaid(id, metaid):
    retval = state.mms.get_metadata_from_metaid(metaid)
    return expect_non_empty_map_return_as_json(retval)


@app.route('/media/id/<id>', methods = ['GET'])
@requires_auth
@catches_model_exception
def get_metadata_from_id(id):
    "Get all the metadata for a particular media id."

    retval = state.mms.get_metadata_from_id(id)
    return expect_non_empty_map_return_as_json(retval)

## XXX This should only be allowed on existing media instances.
##     If the media instance does not already exist, then 
##     /media/metatype/<metatype>  [POST] is what should be used
##     instead.  The way this is designed is just a receipe for disaster.
@app.route('/media/id/<id>/metatype/<metatype>', methods = ['POST'])
@requires_auth
@catches_model_exception
def post_new_meta(id, metatype):
    "Post a new bit of metadata for a media item"
    payload = request.json
    retval = state.mms.store_new_meta_from_id_and_type(id, metatype, payload)
    return expect_non_empty_map_return_as_json(retval)


@app.route('/media/metatype/<metatype>', methods = ['POST'])
@requires_auth
@catches_model_exception
def post_new_meta_with_metatype_only(metatype):
    "Post a new bit of metadata for a media item"
    payload = request.json
    retval = state.mms.store_new_meta_from_type(metatype, payload)
    return expect_non_empty_map_return_as_json(retval,status=201)



@app.route('/media/id/<id>/metaid/<metaid>', methods = ['POST'])
@requires_auth
@catches_model_exception
def post_meta(id, metaid):
    "Post a particular metadata instance"
    retval = state.mms.store_meta(id, metaid)
    return expect_non_empty_map_return_as_json(retval)


# XXX The id is in fact not necessary, and should be
#     removed.
@app.route('/media/id/<id>/metaid/<metaid>', methods = ['DELETE'])
@requires_auth
@catches_model_exception
def delete_meta(id, metaid):
    "Delete a particular metadata instance"
    retval = state.mms.delete_metaid(metaid)
    return expect_non_empty_map_return_as_json(retval)



###
###  Accessing the task queue
###

@app.route('/task/waiting', methods = ['GET'])
@requires_auth
@catches_model_exception
def list_all_waiting_tasks():
    waiting_tasks = state.tqs.list_all_waiting_tasks()
    return expect_non_empty_map_return_as_json(waiting_tasks)

@app.route('/task/running', methods = ['GET'])
@requires_auth
@catches_model_exception
def get_in_progress_task_list():
    running_tasks = state.tqs.list_all_running_tasks()
    returnvalue = expect_non_empty_map_return_as_json(running_tasks)
    return returnvalue

        
@app.route('/task/type/<type>/done', methods = ['GET'])
@requires_auth
@catches_model_exception
def get_done_task_list(type):
    return_value = state.tqs.list_all_done_tasks()
    commit_db()
    return return_value

@app.route('/task/waiting/type/<type>', methods = ['GET'])
@requires_auth
@catches_model_exception
def list_waiting_task_of_type(type):
    waiting_tasks = state.tqs.list_all_waiting_tasks_of_type(type)
    return expect_non_empty_map_return_as_json(waiting_tasks)
        
@app.route('/task/waiting/type/<type>/pick', methods = ['POST'])
@requires_auth
@catches_model_exception
def pick_next_waiting_task(type):
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
@catches_model_exception
def declare_task_as_done(id):
    tqs=state.tqs
    retval = tqs.declare_as_done(id)
    return expect_empty_map_return_error_as_json(retval)
    
@app.route('/task/type/<type>', methods = ['POST'])
@requires_auth
@catches_model_exception
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
@catches_model_exception
def delete_task(taskid):
    retval = state.tqs.delete_task(taskid)
    return expect_empty_map_return_error_as_json(retval)
