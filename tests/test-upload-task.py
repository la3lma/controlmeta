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

# pick up the task ID from the response
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



