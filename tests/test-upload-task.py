#!/usr/bin/python

import sys
import requests
import json


class  ControlMetaClient:
    JSON_HEADERS = {'content-type': 'application/json'}

    def __init__(self, base_url=None):
      self.base_url=base_url

    def upload_task(self, type, parameters):
        tasktypepath = "task/type/%s" % type
        posturl = "%s%s" %(base_url, tasktypepath)
        print "posturl = ", posturl
        response = requests.post(posturl, data=json.dumps(parameters), headers=self.JSON_HEADERS)
        print response
        print response.text
        return json.loads(response.text)
      
    
## Parsing command line parameters
# XXX Add some tests here to check the input parameter
# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)
base_url=str(sys.argv[1])

cmclient = ControlMetaClient(base_url)

print "Testing against base-url = ", base_url
json_headers = {'content-type': 'application/json'}



parameters={'parameter1':'Value 1'}
data = cmclient.upload_task("face", parameters)
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



