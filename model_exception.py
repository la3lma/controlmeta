
class ModelException(Exception):

    def __init__(self,  message, http_returnvalue = None):
        self.http_returnvalue = http_returnvalue
        self.message = message

    def __str__(self):
        return repr(self.message + " -> http code " + str(self.http_returnvalue))

