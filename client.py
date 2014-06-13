import requests
import json

class  UploadResult:
    def __init__(self, document_id, document_url):
        self.document_id = document_id
        self.document_url = document_url
        

    
class ClientException(Exception):

    httpcode=None
    def __init__(self, httpcode, message):
        self.httpcode=httpcode
        self.value = "HTTP return code %s: %s" % (str(httpcode), message)

    def __str__(self):
        return repr(self.value)

    
class  ControlMetaClient:
    JSON_HEADERS = {'content-type': 'application/json'}

    def __init__(self,
                 base_url=None,
                 auth=None):
        if base_url and not base_url.endswith("/"):
            base_url = base_url + "/"

        self.base_url = base_url
        self.auth = auth

    def process(self, function,  url, payload, expected_status, error_message):

        print "process function ", function
        print "process url  ", url

        if payload:
            raw_response  = function(
                url,
                auth=self.auth,
                data=json.dumps(payload),
                headers=self.JSON_HEADERS)
        else:
            raw_response  = function(
                url,
                auth=self.auth,
                headers=self.JSON_HEADERS)


        print "process got raw_response = ", raw_response
        print "Expecting status = ", expected_status

        status_code = raw_response.status_code
        if status_code != expected_status:
            raise ClientException(
                    status_code, 
                    error_message)

        # If there was no content, then return none
        if not raw_response.text:
            return None

        # Since thee was a response we will assume it was
        # json and interpret it as such, and return the
        # interpretation as a collection (or list, or whatever :-)

        print "returning raw_response = ", raw_response
        print "returning raw_response.text = ", raw_response.text

        json_response = json.loads(raw_response.text)

        print "returning raw_response.json = ", json_response

        return json_response


    def post(self, url, payload, expected_status, error_message):
        return self.process(requests.post,
                            url, payload, expected_status, error_message)

    def get(self, url,  expected_status, error_message):
        return self.process(requests.get,
                            url, None, expected_status, error_message)

    def delete(self, url, payload, expected_status, error_message):
        return self.process(requests.delete, 
                            url, payload, expected_status, error_message)

    def all_tasks(self):
        url = "%stask" %(self.base_url)
        return self.get(url,  200, "Unable to get task list")
        
    def upload_task(self, type, parameters):
        tasktypepath = "task/type/%s" % type
        url = "%s%s" %(self.base_url, tasktypepath)
        return self.post(url, parameters, 201, "Unable to upload task")


    def pick_task(self, type, agent_id):
        parameters = {'agentId':agent_id}
        url = "%stask/waiting/type/%s/pick" %(self.base_url, type)
        error_message = "Unable to pick task of type %s for agent %s"%(type, agent_id)
        return self.post(url, parameters, 200, error_message)
        
    def declare_task_done(self, task_id, agent_id):
        print "Client: declaring task done ", task_id
        url="%stask/id/%s/done" %(self.base_url, task_id)
        payload={'agentId': agent_id}
        error_message="Unable to declare task " + str(task_id) + " as done."
        return self.post(url, payload,  204, error_message)

    def upload_metadata(self, type, data):
        url="%s,media/metadata/%s" %(self.base_url, type)
        error_message="Unable to create naked  metadata instance."
        raw_response = self.post(url, data, 204, error_message)
        return json.loads(raw_response.text)

    def upload_media_from_file(self, type, filepath):
        url="%smedia/" %(self.base_url)
        with open(filepath, 'r') as content_file:
            content = content_file.read()
            return self.upload_media(type, content)
    
    # Upload unidentified metadata, get a data ID back
    # XXX Rewrite using the post method.
    def  upload_media(self, type, data):
        url="%smedia/" %(self.base_url)
        raw_response = requests.post(
            url,
            auth=self.auth,
            data=data,
            headers= {'content-type': type})
        jrv=json.loads(raw_response.text)
        return UploadResult(jrv['ContentId'], jrv['ContentURL'])
