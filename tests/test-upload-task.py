#!/usr/bin/python

import sys
import requests
import json

## Parsing command line parameters
# XXX Add some tests here to check the input parameter
# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)
base_url=str(sys.argv[1])
tasktypepath="task/type/face"

print "Testing against base-url = ", base_url
json_headers = {'content-type': 'application/json'}


def upload_task(type, parameters):
    tasktypepath = "task/type/%s" % type
    posturl = "%s%s" %(base_url, tasktypepath)
    print "posturl = ", posturl
    response = requests.post(posturl, data=json.dumps(parameters), headers=json_headers)
    print response
    print response.text
    return json.loads(response.text)

## First upload a task with some parameters
# posturl="%s%s" %(base_url, tasktypepath)
parameters={'parameter1':'Value 1'}

# json_headers = {'content-type': 'application/json'}

# response = requests.post(posturl, data=json.dumps(payload), headers=json_headers)
# print response
# print response.text

data = upload_task("face", parameters)
task_id=data['taskId']

print "taskId=",task_id

## Then pick a task
print "Picking."
agent_id={'agentId':'007'}
pickurl="%s%s" %(base_url, 'task/waiting/type/face/pick')
pickresponse = requests.post(pickurl, data=json.dumps(agent_id), headers=json_headers)
picked_task_id=json.loads(pickresponse.text)['taskId']

print "pickresponse = ", pickresponse
print "pickresponse.text = ", pickresponse.text
print "picked task id", picked_task_id


## And declare it as done
pickurl="%s%s%s" %(base_url, 'task/id/', picked_task_id)
deletedresponse= requests.delete(pickurl, data=json.dumps(agent_id), headers=json_headers)
print "deletedresponse = ", deletedresponse
print "deletedresponse.text = ", deletedresponse.text



