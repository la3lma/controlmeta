#!flask/bin/python
from flask import Flask, jsonify, Response, request, abort
from smsservice import SmsService
import json

smss = SmsService()

app = Flask(__name__)

###
### Media CRUD
###

@app.route('/media', methods = ['GET'])
def get_all_media():
    "Get a list of all the available media."
    return Response(status=500)

@app.route('/media/id/<id>/media', methods = ['GET'])
def get_media(id):
    "Get the media representation of identified asset"
    return Response(status=500)

@app.route('/media/id/<id>/media', methods = ['POST'])
def post_media(id):
    "Write the media representation an identified asset"
    return Response(status=500)

@app.route('/media/id/<id>', methods = ['DELETE'])
def delete_media_and_meta(id):
    "Delete both media and metadata for an identified asset"
    return Response(status=500)

@app.route('/media/id/<id>', methods = ['DELETE'])
def delete_media(id):
    "Delete both media for an identified asset"
    return Response(status=500)


##
##  Meta CRUD
##
@app.route('/media/id/<id>/meta/<metatype>', methods = ['GET'])
def get_meta_list(id, metatype):
    "Get list of metadata assets associated with a media asset"
    return Response(status=500)

@app.route('/media/id/<id>/metaid/<metaid>', methods = ['GET'])
def get_meta(id, metaid):
    "Get a particular metadata instance"
    return Response(status=500)

@app.route('/media/id/<id>/metatype/<metatype>', methods = ['POST'])
def post_new_meta(id, metatype):
    "Get list of metadata assets associated with a media asset"
    return Response(status=500)

@app.route('/media/id/<id>/metaid/<metaid>', methods = ['POST'])
def post_meta(id, metaid):
    "Post a particular metadata instance"
    return Response(status=500)

@app.route('/media/id/<id>/metaid/<metaid>', methods = ['DELETE'])
def delete_meta(id, metaid):
    "Get a particular metadata instance"
    return Response(status=500)

@app.route('/media/id/<id>/meta/<metatype>', methods = ['DELETE'])
def delete_meta_for_id(id, metatype):
    "Delete all metadata of a particular type for a specific media item"
    return Response(status=500)
    
###
###  Accessing the task queue
###

@app.route('/task/type/<type>/waiting/next', methods = ['GET'])
def get_next_waiting_task(type):
    return Response(status=500)
        
@app.route('/task/type/<type>/waiting/pick', methods = ['POST'])
def pick_next_waiting_task(type):
    return Response(status=500)
        
@app.route('/task/type/<type>/in-progress', methods = ['GET'])
def get_in_progress_task_list(type):
    return Response(status=500)
        
@app.route('/task/type/<type>/done', methods = ['POST'])
def get_done_task_list(type):
    return Response(status=500)


##  XXX Deletes are not added

if __name__ == '__main__':
    app.run(debug = True)
