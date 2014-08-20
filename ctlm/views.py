import json
import sys

from flask import jsonify

from ctlm import app
from database import db_session, commit_db
from mediameta.model import RDBMSMediaAndMetaStorage
from model_exception import ModelException
from task.model import RDBQueueStorage
from users.model import UserStorage
import config
import os


# A class to hold a singleton instance. That instance                                  
# holds the state of the application.                                                  
# XXX This is a kludge, for sure.

# Promote into a separate class perhaps?
class State:
    def __init__(self):
        base_url = config.DEFAULT_HOME_URL
        if len(sys.argv) > 1:
            base_url = str(sys.argv[1])
        self.mms = RDBMSMediaAndMetaStorage(base_url)
        self.tqs = RDBQueueStorage()
        self.us = UserStorage(base_url)

    def clean(self):
        self.mms.clean()
        self.mms.clean()
        self.tqs.clean()
        self.us.clean()


state = State()

# XXX This stuff for bootstrapping usernames/passwords is a kludge
# a symptom of bad design that should be fixed asap, after it
#     works!

def bootstrap_username_password(username, password):
    print("bootstrap_username_password(%r, %r)" % (username, password))
    user = state.us.find_user_by_email(username)
    if not user:
        print("bootstrap_username_password: Creating user %r" % username)
        state.us.new_user_with_password(username, password)
        commit_db()
    else:
        print("bootstrap_username_password: User %r already exists." % username)
        print(" User is %r" % user)
        print("All users (1)= %r" % state.us.find_all_users())


def reset_username_and_password():
    print("Bootstrapping user database")
    username = None
    password = None

    if 'USERNAME' in os.environ:
        username = os.environ["USERNAME"]

    if 'PASSWORD' in os.environ:
        password = os.environ["PASSWORD"]

    if username and password:
        bootstrap_username_password(username, password)
        print ("Committing bootstrap parameters")
        commit_db()
    else:
        print("Server found no bootstrap username/password parameters")


def dump_users_to_stdout(msg):
    print("dump_users_to_stdout %r" % msg)
    print("All users (2) = %r" % state.us.find_all_users())


# #
# # Helper functions to make it simpler to translate return values
# # into response objects.
##

def response_as_json(return_value, status=200):
    if not return_value:
        return_value = {}

    commit_db()

    json_dump = json.dumps(return_value)
    response = Response(json_dump, status=status, mimetype="application/json")

    # XXX Why is this commented out?  Can't grok it, should I nuke it?
    #   response = jsonify(retval)
    #   response.status_code = status
    return response


def expect_non_empty_map_response_as_json(return_value, error_code=404, status=200):
    """
    :rtype : object
    """
    if not return_value:
        return Response(status=error_code)
    else:
        commit_db()
        return Response(json.dumps(return_value), status=status, mimetype="application/json")


def allow_empty_map_response_as_json(return_value, status=200):
    commit_db()
    assert isinstance(return_value, object)
    if not return_value:
        return Response(status=status)
    else:
        return Response(json.dumps(return_value), status=status, mimetype="application/json")


def expect_empty_map_return_error_as_json(return_value, status=204, error_code=404):
    if not bool(return_value):
        commit_db()
        return Response(status=status)
    else:
        # XXX The "use a map as a datastructure" antipattern, evaluate and refactor.
        if "HTTP_error_code" in return_value:
            error_code = return_value["HTTP_error_code"]
        return_value_as_json = json.dumps(return_value)
        return Response(return_value_as_json, status=error_code, mimetype="application/json")


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
    password combination is valid."""
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

        elif not state.us.check_auth(auth.username, auth.password):

            print("Failed to authenticate %r/%r" % (auth.username, auth.password))
            print("All users (3)= %r" % state.us.find_all_users())
            return authenticate()

        else:
            request.authenticated_user = \
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

@app.route('/media', methods=['GET'])
@requires_auth
@catches_model_exception
def get_all_media():
    """Get a list of all the available media's metadata."""
    return_value = state.mms.get_all_media()
    return response_as_json(return_value)


@app.route('/media/id/<media_id>', methods=['GET'])
@requires_auth
@catches_model_exception
def get_media(media_id):
    """Get the media representation of identified asset"""
    mime_type, data = state.mms.get_media(media_id)
    if not mime_type:
        return Response(status=404)
    else:
        return Response(data, mimetype=mime_type, status=200)


@app.route('/media/id/<media_id>/exists', methods=['GET'])
@requires_auth
@catches_model_exception
def exists_media(media_id):
    """Get the media representation of identified asset"""
    exists = state.mms.exists_media(media_id)
    if not exists:
        return Response(status=404)
    else:
        return Response(status=200)

def get_authenticated_user():
    # We're all consenting adults here, so this kind of type-unsafeish
    # behavior is acceptable(ish).
    return request.authenticated_user

@app.route('/media/', methods=['POST'])
@requires_auth
@catches_model_exception
def create_new_media_entry_from_upload():
    """Write the media representation an unidentified asset, returns the asset ID"""

    return_value = state.mms.create_new_media_entry(
        request.mimetype,
        request.data,
        get_authenticated_user())
    return response_as_json(return_value, status=201)


@app.route('/media/id/<media_id>', methods=['POST'])
@requires_auth
@catches_model_exception
def post_media_to_id(media_id):
    """Write the media representation an identified asset"""
    return_value = state.mms.post_media_to_id(
        media_id,
        request.mimetype,
        request.data,
        get_authenticated_user())
    return allow_empty_map_response_as_json(return_value, status=201)


@app.route('/media/id/<media_id>/supplement-meta/<meta_id>', methods=['POST'])
@requires_auth
@catches_model_exception
def post_supplement_meta_with_media(media_id, meta_id):
    """Write the media representation an identified asset"""
    return_value = state.mms.supplement_media_to_meta(media_id, meta_id, get_authenticated_user())
    return expect_non_empty_map_response_as_json(return_value, status=200)


@app.route('/media/id/<media_id>', methods=['DELETE'])
@requires_auth
@catches_model_exception
def delete_media_and_meta(media_id):
    """Delete both media and metadata for an identified asset"""
    state.mms.delete_media(media_id, get_authenticated_user())
    commit_db()
    return Response(status=204)


###
###  Meta CRUD
###


@app.route('/media/id/<meta_id>/metatype/<meta_type>', methods=['GET'])
@requires_auth
@catches_model_exception
def get_meta_list_from_id_and_metatype(meta_id, meta_type):
    """Get list of metadata assets associated with a media asset"""
    retval = state.mms.get_metadata_from_id_and_metatype(meta_id, meta_type, get_authenticated_user())
    return response_as_json(retval)


@app.route('/media/metaid/<meta_id>', methods=['GET'])
@requires_auth
@catches_model_exception
def get_metadata_from_metaid(meta_id):
    return_value = state.mms.get_metadata_from_id(
        meta_id,
        get_authenticated_user())
    return response_as_json(return_value)

#XXX These two methods match the same pattern, that must be wrong!

@app.route('/media/id/<media_id>', methods=['GET'])
@requires_auth
@catches_model_exception
def get_metadata_from_id(media_id):
    """Get all the metadata for a particular media id."""
    return_value = state.mms.get_metadata_from_id(
        media_id,
        get_authenticated_user())
    return response_as_json(return_value)


@app.route('/media/id/<media_id>/metatype/<meta_type>', methods=['POST'])
@requires_auth
@catches_model_exception
def post_new_meta(media_id, meta_type):
    """Post a new bit of metadata for a media item"""
    payload = request.json
    return_value = state.mms.store_new_meta_from_id_and_type(
        media_id,
        meta_type,
        payload,
        get_authenticated_user())
    return response_as_json(return_value)



@app.route('/media/metatype/<meta_type>', methods=['POST'])
@requires_auth
@catches_model_exception
def post_new_meta_with_metatype_only(meta_type):
    """Post a new bit of metadata for a media item"""
    payload = request.json
    return_value = state.mms.store_new_meta_from_type(
        meta_type,
        payload,
        get_authenticated_user())
    return response_as_json(return_value, status=201)


@app.route('/media/metaid/<meta_id>', methods=['POST'])
@requires_auth
@catches_model_exception
def post_meta(meta_id):
    """Post to a particular metadata instance"""
    payload = request.json
    return_value = state.mms.update_meta(
        meta_id,
        payload,
        get_authenticated_user())
    return response_as_json(return_value)


@app.route('/media/metaid/<meta_id>', methods=['DELETE'])
@requires_auth
@catches_model_exception
def delete_meta(meta_id):
    """Delete a particular metadata instance"""
    return_value = state.mms.delete_meta_from_id(
        meta_id,
        get_authenticated_user())
    return response_as_json(return_value)


###
###  Accessing the task queue
###

# Get all tasks (for debugging)
@app.route('/task', methods=['GET'])
@requires_auth
@catches_model_exception
def list_all_tasks():
    # XXX Need to send users in to all of these methods too, but
    #     later.
    tasks = state.tqs.list_all_tasks()
    return response_as_json(tasks)


@app.route('/task/waiting', methods=['GET'])
@requires_auth
@catches_model_exception
def list_all_waiting_tasks():
    tasks = state.tqs.list_all_waiting_tasks()
    return response_as_json(tasks)


@app.route('/task/done', methods=['GET'])
@requires_auth
@catches_model_exception
def list_all_done_tasks():
    tasks = state.tqs.list_all_done_tasks()
    return response_as_json(tasks)


@app.route('/task/running', methods=['GET'])
@requires_auth
@catches_model_exception
def get_running_tasks_list():
    tasks = state.tqs.list_all_running_tasks()
    return response_as_json(tasks)


# XXX The state queries are inconsistent

@app.route('/task/type/<task_type>/running', methods=['GET'])
@requires_auth
@catches_model_exception
def get_running_tasks_of_type_list(task_type):
    tasks = state.tqs.list_all_running_tasks_of_type(task_type)
    return response_as_json(tasks)


@app.route('/task/type/<task_type>/done', methods=['GET'])
@requires_auth
@catches_model_exception
def get_done_task_list(task_type):
    return response_as_json(state.tqs.list_all_done_tasks())


@app.route('/task/waiting/type/<task_type>', methods=['GET'])
@requires_auth
@catches_model_exception
def list_waiting_task_of_type(task_type):
    tasks = state.tqs.list_all_waiting_tasks_of_type(task_type)
    return response_as_json(tasks)


@app.route('/task/waiting/type/<task_type>/pick', methods=['POST'])
@requires_auth
@catches_model_exception
def pick_next_waiting_task(task_type):
    # XXX This will fail with a 500 error if the JSON is syntactically bogus
    #     We should test for that and fail gracefully instead
    agent_description = request.json
    if not agent_description:
        data = request.stream.read()
        raise ModelException("Agent description was not legal JSON syntax: '%s' " % data, 400)

    task = state.tqs.pick_next_waiting_task_of_type(task_type, agent_description)
    return response_as_json(task)


@app.route('/task/id/<task_id>', methods=['GET'])
@requires_auth
@catches_model_exception
def get_task_from_id(task_id):
    return_value = state.tqs.get_task(task_id)
    return jsonify(return_value)


@app.route('/task/id/<task_id>/done', methods=['POST'])
@requires_auth
@catches_model_exception
def declare_task_as_done(task_id):
    tqs = state.tqs
    params = request.json
    if not params:
        raise ModelException("No params specified when marking task as done", 400)

    if not 'agentId' in params:
        raise ModelException("No agent specified when marking task as done", 400)

    agent_id = params['agentId']

    return_value = tqs.declare_as_done(task_id, agent_id)
    commit_db()
    return jsonify(return_value)


@app.route('/task/type/<task_type>', methods=['POST'])
@requires_auth
@catches_model_exception
def create_task(task_type):
    params = request.json
    if not params:
        params = request.stream.read()
        raise ModelException("Agent description was not legal JSON syntax: '%s' " % request.data, 400)
    return_value = state.tqs.create_task(task_type, params)
    return response_as_json(return_value, status=201)


@app.route('/task/id/<task_id>', methods=['DELETE'])
@requires_auth
@catches_model_exception
def delete_task(task_id):
    return_value = state.tqs.delete_task(task_id)
    return expect_empty_map_return_error_as_json(return_value)


# XXX This method is not reachable through the web server.  Why not?
# @requires_auth
@app.route('/users', methods=['GET'])
@catches_model_exception
def get_users():
    print("server:get_users was hit")
    state.us.report()
    return_value = state.us.find_all_users()
    print("server:get_users returning users = %r" % return_value)
    return allow_empty_map_response_as_json(return_value)


#  XXXX Very bogus, only for use during debugging, should be disabled in production!
# @requires_auth
@app.route('/reset', methods=['GET'])
@catches_model_exception
def reset_users():
    print("server:reset_users was hit")
    reset_username_and_password()
    return get_users()

# XXX More user management needed, all of it is missing :-)
