# This works somewhat with acceptance tests, but fails some unit tests.
# SQLALCHEMY_DATABASE_URI='sqlite:///testdb.db'

# This works perfectly with the unit tests, but fails
# the acceptance tests.
SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'

# XXX This sensitivity is discuraging.
