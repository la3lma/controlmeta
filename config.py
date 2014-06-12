
# import os


###
### XXX This is site-specific and context-specific config
###     it should not be in a version-controlled file
###

##
## Setting up the default database
##
# This works with acceptance tests, but fails some unit tests.
SQLALCHEMY_DATABASE_URI='sqlite:///testdb.db'

# This works perfectly with the unit tests, but fails
# the acceptance tests.
# SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'



##
## Setting up the default home URL
##
DEFAULT_HOME_URL="http://ctlmeta.loltel.co"



