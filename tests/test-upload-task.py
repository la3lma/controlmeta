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
        response = requests.post(posturl, data=json.dumps(parameters), headers=self.JSON_HEADERS)
        # XXX Some checking of return values and perhaps throwing
        #     of exceptions?
        return json.loads(response.text)

    def pick_task(self, type, agent_id):
        print "Picking."
        agent_id={'agentId':agent_id}
        pickurl="%stask/waiting/type/%s/pick" %(base_url, type)
        pickresponse = requests.post(pickurl, data=json.dumps(agent_id), headers=json_headers)
        return json.loads(pickresponse.text)

    def declare_task_done(self, task_id, agent_id):
        pickurl="%s%s%s" %(base_url, 'task/id/', task_id)
        agent_id={'agentId': agent_id}
        raw_response = requests.delete(pickurl, data=json.dumps(agent_id), headers=json_headers)
        return raw_response

      
    
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
# agent_id={'agentId':'007'}
# pickurl="%s%s" %(base_url, 'task/waiting/type/face/pick')
# pickresponse = requests.post(pickurl, data=json.dumps(agent_id), headers=json_headers)

pickresponse=cmclient.pick_task('face', '007')

print "pickresponse = ", pickresponse
picked_task_id=pickresponse['taskId']
print "picked task id", picked_task_id


## And declare it as done

deletedresponse=cmclient.declare_task_done(picked_task_id, '007')

print "deletedresponse = ", deletedresponse
print "deletedresponse.text = ", deletedresponse.text



