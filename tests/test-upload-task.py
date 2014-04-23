#!/usr/bin/python

import sys
import client

    

base_url=str(sys.argv[1])

cmclient = client.ControlMetaClient(base_url)

print "Testing against base-url = ", base_url
json_headers = {'content-type': 'application/json'}

parameters={'parameter1':'Value 1'}
data = cmclient.upload_task("face", parameters)
task_id=data['taskId']

print "taskId=",task_id

## Then pick a task

print "Picking."
pickresponse=cmclient.pick_task('face', '007')
print "pickresponse = ", pickresponse
picked_task_id=pickresponse['taskId']
print "picked task id", picked_task_id


## And declare it as done

deletedresponse=cmclient.declare_task_done(picked_task_id, '007')

print "deletedresponse = ", deletedresponse
print "deletedresponse.text = ", deletedresponse.text



