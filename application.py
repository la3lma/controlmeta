#/usr/bin/python

import flask
import ctlm
application = ctlm.application
app=application

#Set application.debug=true to enable tracebacks on Beanstalk log output. 
#Make sure to remove this line before deploying to production.
# XXX This thing should be imported through a config file, not set
#     in the application like this.
application.debug=True


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
