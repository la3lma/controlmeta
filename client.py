import requests
import json

class  UploadResult:

    def __init__(self, document_id, document_url):
        self.document_id = document_id
        self.document_url = document_url
    

    
class  ControlMetaClient:
    JSON_HEADERS = {'content-type': 'application/json'}
    def __init__(self, base_url=None):
      self.base_url=base_url


    def post_dictionary_as_json(self, url, dictionary):
        raw_response = requests.post(
            url,
            data=json.dumps(dictionary),
            headers=self.JSON_HEADERS)
        return json.loads(raw_response.text)
        
    def upload_task(self, type, parameters):
        tasktypepath = "task/type/%s" % type
        url = "%s%s" %(self.base_url, tasktypepath)
        return post_dictionary_as_json(
            url,
            parameters)

    def pick_task(self, type, agent_id):
        print "Picking."
        parameters={'agentId':agent_id}
        url="%stask/waiting/type/%s/pick" %(self.base_url, type)
        return post_dicctionary_as_json(
            pickurl,
            parameters)

    def declare_task_done(self, task_id, agent_id):
        pickurl="%s%s%s" %(self.base_url, 'task/id/', task_id)
        parameters={'agentId': agent_id}
        raw_response = requests.delete(
                pickurl,
                data=json.dumps(parameters),
                headers=self.JSON_HEADERS)
        # XXX Return value
        return raw_response

    # Upload unidentified metadata, get a metadata ID back
    def upload_metadata(self, type, data):
        ## This is fXed up
        raw_response = requests.post(
            url,
            headers=self.JSON_HEADERS,
            data=json.dumps(data))
        # XXX return value not correctly parsed
        return raw_response

    # Upload unidentified metadata, get a data ID back
    def  upload_media(self, type, data):
        url="%smedia/" %(self.base_url)
        raw_response = requests.post(
            url,
            data=data,
            headers= {'content-type': 'application/json'})
        jrv=json.loads(raw_response.text)
        return UploadResult(jrv['ContentId'], jrv['ContentURL'])
    
    def  upload_media_file(self, type, filename):
        print "uploading data type", type
        print "uploading data filename", filename
        
