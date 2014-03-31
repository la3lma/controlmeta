#!flask/bin/python
from flask import Flask, jsonify, Response, request, abort
from smsservice import SmsService
import json

smss = SmsService()

app = Flask(__name__)

###
###  Media and meta CRUD
###

@app.route('/media/id/<id>/media', methods = ['GET'])
def get_service_configuration():
        Response(status=500)

@app.route('/media/id/<id>/meta/{metatype}', methods = ['GET'])
def get_service_configuration(id, metatype):
        Response(status=500)

@app.route('/media/id/<id>/media', methods = ['POST'])
def post_user_provisioning(id):
        Response(status=500)

@app.route('/media/id/<id>/meta/<metatype>', methods = ['POST'])
def post_user_provisioning(id, metatype):
        Response(status=500)

@app.route('/media/id/<id>/meta/<metatype>', methods = ['POST'])
def post_user_provisioning(id, metatype):
        Response(status=500)

##  XXX Deletes are not added

###
###  Accessing the task queue
###

@app.route('/task/type/<type>/waiting/next', methods = ['GET'])
def get_next_waiting_task(type):
        Response(status=500)
        
@app.route('/task/type/<type>/waiting/pick', methods = ['POST'])
def pick_next_waiting_task(type):
        Response(status=500)
        
@app.route('/task/type/<type>/in-progress/list', methods = ['GET'])
def get_in_progress_task_list(type):
        Response(status=500)
        
@app.route('/task/type/<type>/done/list', methods = ['POST']
def get_done_task_list(type):
        Response(status=500)


##  XXX Deletes are not added

if __name__ == '__main__':
    app.run(debug = True)

