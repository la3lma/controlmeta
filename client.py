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

    def post(self, url, payload, expected_status, error_message):
        raw_response  = requests.delete(
                url,
                auth=self.auth,
                data=json.dumps(payload),
                headers=self.JSON_HEADERS)
        status_code = raw_response.status_code
        if status_code != expected_status:
            raise ClientException(
                    status_code, 
                    error_message)
        return raw_response


    def post_dictionary_as_json(self, url, dictionary):
        raw_response = requests.post(
            url,
            auth=self.auth,
            data=json.dumps(dictionary),
            headers=self.JSON_HEADERS)
        if raw_response.status_code == 500:
            raise ClientException(500, "Unable to post a dictionary to url = %s"%url)
        if raw_response.status_code == 401:
            raise ClientException(401, raw_response.text)
        else:
            return json.loads(raw_response.text)
        
    def upload_task(self, type, parameters):
        tasktypepath = "task/type/%s" % type
        url = "%s%s" %(self.base_url, tasktypepath)
        self.post(url, parameters, 204, "Unable to upload task")


    def pick_task(self, type, agent_id):
        parameters = {'agentId':agent_id}
        url = "%stask/waiting/type/%s/pick" %(self.base_url, type)
        error_message = "Unable to pick task of type %s for agent %s"%(type, agentid)
        post(url, parameters, 200, error_message)

        
    def declare_task_done(self, task_id, agent_id):
        url="%s%s%s" %(self.base_url, 'task/id/', task_id)
        payload={'agentId': agent_id}
        error_message="Unable to declare task " + str(task_id) + " as done."
        self.post(url, payload,  204, error_message)


    def upload_metadata(self, type, data):
        url="%s,media/metadata/%s" %(self.base_url, type)
        error_message="Unable to create naked  metadata instance."
        raw_response = self.post(url, data, 204, error_message)
        return json.loads(raw_response.text)


    def  upload_media_from_file(self, type, filepath):
        url="%smedia/" %(self.base_url)
        with open(filepath, 'r') as content_file:
            content = content_file.read()
            return self.upload_media(type, content)
    
    # Upload unidentified metadata, get a data ID back
    def  upload_media(self, type, data):
        url="%smedia/" %(self.base_url)
        raw_response = requests.post(
            url,
            auth=self.auth,
            data=data,
            headers= {'content-type': type})
        jrv=json.loads(raw_response.text)
        return UploadResult(jrv['ContentId'], jrv['ContentURL'])
