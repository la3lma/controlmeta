#!/usr/bin/python

import sys
import client
from requests.auth import HTTPBasicAuth
    
# Pick a base url from the command line
base_url=str(sys.argv[1])

# Use the very secret admin password for testing
auth=HTTPBasicAuth('admin','secret')

# Then set up a client against that server
cmc = client.ControlMetaClient(base_url, auth=auth)

# Upload a task of type "face" with some parameters.
print "Testing against base-url = ", base_url
parameters={'parameter1':'Value 1'}
data = cmc.upload_task("face", parameters)

print "Pre getting tasks"
t1=cmc.all_tasks()
print "Tasks 1 = ", t1

print " data -> ", data
# pick up the task ID from the response
task_id = data.task_id
print "taskId=",task_id

## Then pick a task

print "Picking."
pickresponse=cmc.pick_task('face', '007')
print "pickresponse = ", pickresponse
picked_task_id=pickresponse['taskId']
print "picked task id", picked_task_id

foo=cmc.all_tasks()
print "Tasks 2 -> = ", foo

## And declare it as done
doneresponse = cmc.declare_task_done(picked_task_id, '007')

t3=cmc.all_tasks()
print "Tasks 3 = ", t3


