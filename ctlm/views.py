from flask import  jsonify, Response, request, abort
import json
import sys

from ctlm import app
from database import Base, db_session, init_db, commit_db
from mediameta.model import RDBMSMediaAndMetaStorage
from model_exception import ModelException
from task.model import RDBQueueStorage
from users.model import UserStorage
import config

import logging
logging.basicConfig(level=logging.DEBUG)

# A class to hold a singleton instance. That instance                                  
# holds the state of the application.                                                  
# XXX This is a kludge, for sure.

# Promote into a separate class perhaps?
class State:

    def __init__(self):
        base_url=config.DEFAULT_HOME_URL
        if (len(sys.argv) > 1):
            base_url=str(sys.argv[1])
        self.mms = RDBMSMediaAndMetaStorage(base_url)
        self.tqs = RDBQueueStorage()
        self.us  = UserStorage(base_url)


state = State()

##
## Helper functions to make it simpler to translate return values
## into response objects.
##

def response_as_json(retval, status=200):

    if not retval:
        retval = {}

    commit_db()

    json_dump = json.dumps(retval)
    response =  Response(json_dump, status=status, mimetype="application/json")

# XXX Why is this commented out?  Can't grok it, should I nuke it?
#   response = jsonify(retval)
#   response.status_code = status
    return response


def expect_non_empty_map_response_as_json(retval, errorcode=404, status=200):
    if (not retval):
        return Response(status=errorcode)
    else:
        commit_db()
        return Response(json.dumps(retval), status=status, mimetype="application/json")

def allow_empty_map_response_as_json(retval, status=200):
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

        elif  not state.us.check_auth(auth.username, auth.password):
            return authenticate()

        else:
            request.authenticated_user =  \
                 state.us.find_user_by_email(auth.username)
            
            return f(*args, **kwargs)
    return decorated



def catches_model_exception(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ModelException as e:
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
@catches_model_exception
def get_all_media():
     "Get a list of all the available media's metadata."
     retval=state.mms.get_all_media()
     return response_as_json(retval)

@app.route('/media/id/<id>', methods = ['GET'])
@requires_auth
@catches_model_exception
def get_media(id):
     "Get the media representation of identified asset"
     mimetype, data = state.mms.get_media(id)
     if (not mimetype):
         return Response(status=404)
     else:
         return Response(data, mimetype=mimetype, status=200)


@app.route('/media/id/<id>/exists', methods = ['GET'])
@requires_auth
@catches_model_exception
def exists_media(id):
     "Get the media representation of identified asset"
     exists = state.mms.exists_media(id)
     if (not exists):
         return Response(status=404)
     else:
         return Response(status=200)


@app.route('/media/', methods = ['POST'])
@requires_auth
@catches_model_exception
def create_new_media_entry_from_upload():
     "Write the media representation an unidentified asset, returns the asset ID"
     
     user = request.authenticated_user

     retval = state.mms.create_new_media_entry(request.mimetype, request.data, user)
     return response_as_json(retval, status=201)

@app.route('/media/id/<id>', methods = ['POST'])
@requires_auth
@catches_model_exception
def post_media_to_id(id):
    "Write the media representation an identified asset"
    user = request.authenticated_user
    returnvalue = state.mms.post_media_to_id(id, request.mimetype, request.data, user)
    return allow_empty_map_response_as_json(returnvalue, status=201)

@app.route('/media/id/<mediaid>/supplement-meta/<metaid>', methods = ['POST'])
@requires_auth
@catches_model_exception
def post_supplement_meta_with_media(mediaid, metaid):
    "Write the media representation an identified asset"
    user = request.authenticated_user
    returnvalue = state.mms.supplement_media_to_meta(mediaid, metaid, user)
    return expect_non_empty_map_response_as_json(returnvalue, status=200)


@app.route('/media/id/<id>', methods = ['DELETE'])
@requires_auth
@catches_model_exception
def delete_media_and_meta(id):
    "Delete both media and metadata for an identified asset"
    user = request.authenticated_user
    state.mms.delete_media(id, user)
    commit_db()
    return Response(status=204)

###
###  Meta CRUD
###


@app.route('/media/id/<id>/metatype/<metatype>', methods = ['GET'])
@requires_auth
@catches_model_exception
def get_meta_list_from_id_and_metatype(id, metatype):
    "Get list of metadata assets associated with a media asset"
    user = request.authenticated_user
    retval = state.mms.get_metadata_from_id_and_metatype(id, metatype, user)
    return response_as_json(retval)

@app.route('/media/metaid/<metaid>', methods = ['GET'])
@requires_auth
@catches_model_exception
def get_metadata_from_metaid(metaid):
    user = request.authenticated_user
    retval = state.mms.get_metadata_from_id(metaid, user)
    return response_as_json(retval)


@app.route('/media/id/<id>', methods = ['GET'])
@requires_auth
@catches_model_exception
def get_metadata_from_id(id):
    "Get all the metadata for a particular media id."
    user = request.authenticated_user
    retval = state.mms.get_metadata_from_id(id, user)
    return response_as_json(retval)


@app.route('/media/id/<id>/metatype/<metatype>', methods = ['POST'])
@requires_auth
@catches_model_exception
def post_new_meta(id, metatype):
    "Post a new bit of metadata for a media item"
    payload = request.json
    user = request.authenticated_user
    retval = state.mms.store_new_meta_from_id_and_type(id, metatype, payload, user)
    return response_as_json(retval)


@app.route('/media/metatype/<metatype>', methods = ['POST'])
@requires_auth
@catches_model_exception
def post_new_meta_with_metatype_only(metatype):
    "Post a new bit of metadata for a media item"
    payload = request.json
    user = request.authenticated_user
    retval = state.mms.store_new_meta_from_type(metatype, payload, user)
    return response_as_json(retval,status=201)


@app.route('/media/metaid/<metaid>', methods = ['POST'])
@requires_auth
@catches_model_exception
def post_meta(metaid):
    "Post to a particular metadata instance"
    payload = request.json
    user = request.authenticated_user
    retval = state.mms.update_meta(metaid, request.json, user)
    return response_as_json(retval)


@app.route('/media/metaid/<metaid>', methods = ['DELETE'])
@requires_auth
@catches_model_exception
def delete_meta(id, metaid):
    "Delete a particular metadata instance"
    user = request.authenticated_user
    retval = state.mms.delete_metaid(metaid, user)
    return response_as_json(retval)



###
###  Accessing the task queue
###

# Get all tasks (for debugging)
@app.route('/task', methods = ['GET'])
@requires_auth
@catches_model_exception
def list_all_tasks():
    # XXX Need to send users in to all of these methods too, but
    #     later.
    tasks = state.tqs.list_all_tasks()
    return response_as_json(tasks)

@app.route('/task/waiting', methods = ['GET'])
@requires_auth
@catches_model_exception
def list_all_waiting_tasks():
    tasks = state.tqs.list_all_waiting_tasks()
    return response_as_json(tasks)

@app.route('/task/done', methods = ['GET'])
@requires_auth
@catches_model_exception
def list_all_done_tasks():
    tasks = state.tqs.list_all_done_tasks()
    return response_as_json(tasks)

@app.route('/task/running', methods = ['GET'])
@requires_auth
@catches_model_exception
def get_running_tasks_list():
    tasks = state.tqs.list_all_running_tasks()
    return response_as_json(tasks)


# XXX The state queries are inconsistent

@app.route('/task/type/<tasktype>/running', methods = ['GET'])
@requires_auth
@catches_model_exception
def get_running_tasks_of_type_list(tasktype):
    tasks = state.tqs.list_all_running_tasks_of_type(tasktype)
    return  response_as_json(tasks)

        
@app.route('/task/type/<type>/done', methods = ['GET'])
@requires_auth
@catches_model_exception
def get_done_task_list(type):
    return response_as_json(state.tqs.list_all_done_tasks())


@app.route('/task/waiting/type/<type>', methods = ['GET'])
@requires_auth
@catches_model_exception
def list_waiting_task_of_type(type):
    tasks = state.tqs.list_all_waiting_tasks_of_type(type)
    return  response_as_json(tasks)
        
@app.route('/task/waiting/type/<type>/pick', methods = ['POST'])
@requires_auth
@catches_model_exception
def pick_next_waiting_task(type):
    # XXX This will fail with a 500 error if the JSON is syntactically bogus
    #     We should test for that and fail gracefully instead
    agent_description=request.json
    if not agent_description:
        data = request.stream.read()
        raise ModelException("Agent description was not legal JSON syntax: '%s' "%(data), 400)

    task = state.tqs.pick_next_waiting_task_of_type(type, agent_description)
    return response_as_json(task)


@app.route('/task/id/<id>', methods = ['GET'])
@requires_auth
@catches_model_exception
def get_task_from_id(id):
    retval = state.tqs.get_task(id)
    return  jsonify(retval)


@app.route('/task/id/<id>/done', methods = ['POST'])
@requires_auth
@catches_model_exception
def declare_task_as_done(id):
    tqs = state.tqs
    params=request.json
    if not params:
        raise ModelException("No params specified when marking task as done", 400)

    if  not 'agentId' in params:
        raise ModelException("No agent specified when marking task as done", 400)

    agent_id = params['agentId']

    retval = tqs.declare_as_done(id, agent_id)
    commit_db()
    return  jsonify(retval)


    
@app.route('/task/type/<type>', methods = ['POST'])
@requires_auth
@catches_model_exception
def create_task(type):
    params=request.json
    if not params:
        params = request.stream.read()
        raise ModelException("Agent description was not legal JSON syntax: '%s' "%(data), 400)
    retval = state.tqs.create_task(type, params)
    return response_as_json(retval, status=201)

@app.route('/task/id/<taskid>', methods = ['DELETE'])
@requires_auth
@catches_model_exception
def delete_task(taskid):
    retval = state.tqs.delete_task(taskid)
    return expect_empty_map_return_error_as_json(retval)
