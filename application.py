#/usr/bin/python

import flask
import ctlm
from ctlm.views import bootstrap_username_password, dump_users_to_stdout
import os
from database import commit_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

application = ctlm.application
app=application

#Set application.debug=true to enable tracebacks on Beanstalk log output. 
#Make sure to remove this line before deploying to production.
# XXX This thing should be imported through a config file, not set
#     in the application like this.
application.debug=True

print "About to log"
logger.error("Starting application (3error)")
logger.warning("starting application ()warning)")
logger.debug("Starting application (debug)")
logger.info("Starting application (info)")

print "Just logged %r"%os.environ
dump_users_to_stdout("pre __main__")

if __name__ == '__main__':

    print("starting application")
    username = None
    password = None

    if 'USERNAME' in os.environ:
        username = os.environ["USERNAME"]

    if 'PASSWORD' in os.environ:
        password = os.environ["PASSWORD"]

    if username and password:
        bootstrap_username_password(username, password)
        logging.debug( "Committing bootstrap parameters")
        commit_db()
    else:
        logging.debug("Server found no bootstrap username/password parameters")


    dump_users_to_stdout("pre run")
    application.run(host='0.0.0.0', debug=True)
    dump_users_to_stdout("post run")
else:
    print("Not __main__")

