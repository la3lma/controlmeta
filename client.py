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
        return self.post_dictionary_as_json(
            url,
            parameters)

    def pick_task(self, type, agent_id):
        parameters={'agentId':agent_id}
        url="%stask/waiting/type/%s/pick" %(self.base_url, type)
        return self.post_dictionary_as_json(
            url,
            parameters)

    def declare_task_done(self, task_id, agent_id):
        pickurl="%s%s%s" %(self.base_url, 'task/id/', task_id)
        parameters={'agentId': agent_id}
        raw_response = requests.delete(
                pickurl,
                auth=self.auth,
                data=json.dumps(parameters),
                headers=self.JSON_HEADERS)
        # XXX Return value
        return raw_response

    # Upload unidentified metadata, get a metadata ID back
    def upload_metadata(self, type, data):
        ## This is fXed up
        print "Uploading metadata from url = " , url
        raw_response = requests.post(
            url,
            auth=self.auth,
            headers=self.JSON_HEADERS,
            data=json.dumps(data))
        # XXX return value not correctly parsed
        return raw_response

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
