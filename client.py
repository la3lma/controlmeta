import requests
import json

class  ControlMetaClient:
    JSON_HEADERS = {'content-type': 'application/json'}

    def __init__(self, base_url=None):
      self.base_url=base_url

    def upload_task(self, type, parameters):
        tasktypepath = "task/type/%s" % type
        posturl = "%s%s" %(self.base_url, tasktypepath)
        response = requests.post(posturl, data=json.dumps(parameters), headers=self.JSON_HEADERS)
        # XXX Some checking of return values and perhaps throwing
        #     of exceptions?
        return json.loads(response.text)

    def pick_task(self, type, agent_id):
        print "Picking."
        agent_id={'agentId':agent_id}
        pickurl="%stask/waiting/type/%s/pick" %(self.base_url, type)
        pickresponse = requests.post(pickurl, data=json.dumps(agent_id), headers=self.JSON_HEADERS)
        return json.loads(pickresponse.text)

    def declare_task_done(self, task_id, agent_id):
        pickurl="%s%s%s" %(self.base_url, 'task/id/', task_id)
        agent_id={'agentId': agent_id}
        raw_response = requests.delete(pickurl, data=json.dumps(agent_id), headers=self.JSON_HEADERS)
        return raw_response
