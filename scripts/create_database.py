#!/usr/bin/python

#
# Create a fresh database for test purposes.
#

import database
import task.model
import mediameta.model
import os

fname = 'testdb.db'
if os.path.isfile(fname):
    os.remove(fname)

database.init_db()
