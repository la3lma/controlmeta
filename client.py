import requests
import json

class  Media:
    def __init__(self, document_id, document_url):
        self.document_id = document_id
        self.document_url = document_url

def new_media_result(rv):
    return Media(rv['media_id'], rv['media_url'])


class  Meta:
    def __init__(self, media_id, media_url, meta_id, meta_url, meta_type, meta_content):
        self.media_id = media_id
        self.media_url = media_url
        self.meta_id = meta_id
        self.url = meta_url
        self.type = meta_type
        self.content = meta_content

def new_meta_result(rv):
        return Media(
            rv['media_id'],
            rv['media_url'],
            rv['meta_id'],
            rv['meta_url'],
            rv['meta_type'],
            rv['meta_content'])

class  Task:
    def __init__(self, task_id, status, parameters, task_type):
        self.status = status
        self.parameters = parameters
        self.id = task_id
        self.task_type = task_type


    def __repr__(self):
        return "<Task id:'%r', type:'%r',  status:'%r', parameters:'%r'>" % \
            (self.id, self.task_type, self.status, self.parameters)

def new_task_result(rv):
    if not rv: 
        raise ClientException(None, "Attempt to create task instance from empty dictionary")
    
    # XXX Rewrite to underscored names
    return Task(
        rv['taskId'],
        rv['status'],
        rv['params'],
        rv['taskType']
        )



    
class ClientException(Exception):

    httpcode=None
    def __init__(self, httpcode, message):
        self.httpcode=httpcode
        if httpcode:
            self.value = "HTTP return code %s: %s" % (str(httpcode), message)
        else:
            self.value = message
        
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

        if not payload:
            payload = {}

        raw_response  = function(
                url,
                auth=self.auth,
                data=json.dumps(payload),
                headers=self.JSON_HEADERS)

        status_code = raw_response.status_code
        if status_code != expected_status:
            raise ClientException(
                    status_code, 
                    error_message)

        # If there was no content, then return none

        if not raw_response.text:
            return None

        # Since there was a response we will assume it was
        # json and interpret it as such, and return the
        # interpretation as a collection (or list, or whatever :-)

        return  json.loads(raw_response.text)

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
        task_list = self.get(url,  200, "Unable to get task list")
        return map(new_task_result, task_list)
        
    def upload_task(self, type, parameters):
        tasktypepath = "task/type/%s" % type
        url = "%s%s" %(self.base_url, tasktypepath)
        task  = self.post(url, parameters, 201, "Unable to upload task")
        return new_task_result(task)


    def pick_task(self, type, agent_id):
        parameters = {'agentId':agent_id}
        url = "%stask/waiting/type/%s/pick" %(self.base_url, type)
        error_message = "Unable to pick task of type %s for agent %s"%(type, agent_id)
        task = self.post(url, parameters, 200, error_message)
        return new_task_result(task)
        
    def declare_task_done(self, task_id, agent_id):
        url="%stask/id/%s/done" %(self.base_url, task_id)
        payload={'agentId': agent_id}
        error_message="Unable to declare task " + str(task_id) + " as done."
        task = self.post(url, payload,  200, error_message)
        return new_task_result(task)

    def upload_metadata(self, type, data):
        url="%s/media/metatype/%s" %(self.base_url, type)
        error_message="Unable to create naked  metadata instance."
        raw_response = self.post(url, data, 200, error_message)
        jrv = json.loads(raw_response.text)
        return new_meta_result(jrv)

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
        return new_media_result(jrv)
