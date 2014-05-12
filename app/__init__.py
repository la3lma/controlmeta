from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from database import  init_db
# This weirdness seems to be necessary for elastic beanstalk to 
# be able to recognize the application.
application = Flask(__name__)
app=application

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///:memory:'
db  = SQLAlchemy(app)
init_db()

# A class to hold a singleton instance. That instance
# holds the state of the application.
# XXX This is a kludge.  A sign of bad design. It should e
#     engineered away

# import views.py

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
    state.clear()
