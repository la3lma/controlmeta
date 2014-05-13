#/usr/bin/python

import flask
import app
application = app.application


#Set application.debug=true to enable tracebacks on Beanstalk log output. 
#Make sure to remove this line before deploying to production.
application.debug=True

##  Is this necessary?
import app.views 

 
if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
