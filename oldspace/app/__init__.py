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
