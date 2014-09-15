#!/bin/bash

# Get SQLALCHEMY_DATABASE_URI
. secrets.sh

PYTHON=/usr/bin/python
BASEDIR=$(dirname $0)

(cd "$BASEDIR" && $PYTHON create_database.py)

