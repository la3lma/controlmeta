#!/usr/bin/python

import sys
import client

    

base_url=str(sys.argv[1])

cmc = client.ControlMetaClient(base_url)

print "Testing against base-url = ", base_url
json_headers = {'content-type': 'application/json'}

parameters={'parameter1':'Value 1'}
data = cmc.upload_task("face", parameters)
task_id=data['taskId']

print "taskId=",task_id

## Then pick a task

print "Picking."
pickresponse=cmc.pick_task('face', '007')
print "pickresponse = ", pickresponse
picked_task_id=pickresponse['taskId']
print "picked task id", picked_task_id


## And declare it as done
doneresponse=cmc.declare_task_done(picked_task_id, '007')

print "doneresponse = ", doneresponse
print "doneresponse.text = ", doneresponse.text



