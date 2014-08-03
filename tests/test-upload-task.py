#!/usr/bin/python

import sys
import client
from requests.auth import HTTPBasicAuth
from get_test_auth import get_test_auth


# Pick a base url from the command line
base_url = str(sys.argv[1])

# Get auth parameters from environment variables
auth = get_test_auth()

# Then set up a client against that server
cmc = client.ControlMetaClient(base_url, auth=auth)

# Upload a task of type "face" with some parameters.
parameters = {'parameter1': 'Value 1'}
data = cmc.upload_task("face", parameters)

t1 = cmc.all_tasks()

# pick up the task ID from the response
task_id = data.id

## Then pick a task

pickresponse = cmc.pick_task('face', '007')
picked_task_id = pickresponse.id

foo = cmc.all_tasks()
## And declare it as done
doneresponse = cmc.declare_task_done(picked_task_id, '007')

t3=cmc.all_tasks()


