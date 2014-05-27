from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

## XXX Where will I get the config from?

# XXX Don't delete. Start using instead!!
# def create_app(self):
#    app.config.from_object('config.TestConfiguration')
#    return app


application = Flask(__name__)
app=application

import ctlm.views 


