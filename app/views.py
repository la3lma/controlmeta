from flask import  jsonify, Response, request, abort
import json
import app
import sys 

from database import db_session

app = app.app

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

    
##
##  Static pages
##

@app.route('/')
def hello_world():
    return "lol control meta!"

# The objective of this thing is to make a really minimal
# application that can create new database objects
# (and thus by induction do everything else in a database)
# but can be tested, run locally and possibly even 
# deployed using a real live postgresql database
# in ELB. This is the line going down in the "T".
# The old app did the line at the top, but broke badly
# when adding persistence.    In this incarnation we'll
# run the persistence ting down, and then we'll add the
# rest when we know how this vertical architectural
# spike works out.
@app.route('/newtask')
def newtask():
    return "lol control meta!"

