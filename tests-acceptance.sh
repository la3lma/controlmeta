#!/bin/bash

# Test regression with a full stack, using wire-protocols

# XXX
# The base url is the url the application is running at.
# it is necessary to send in as parameter, since I don't yet
# know how to pick it up from within application.py.
BASE_URL=http://localhost:5000/

PYTHON=/usr/bin/python
# Start the service
$PYTHON application.py "$BASE_URL" &
SERVER_PID=$!


# This is bogus, should wait for the text " * Restarting with reloader" in the
# server's output before proceeding.
sleep 5
# Run the media upload roundtrip-test.
$PYTHON tests/test-upload-media.py $BASE_URL

# Then  the task manipulation roundtrip-test.
$PYTHON tests/test-upload-task.py $BASE_URL

# Finally shut down the server

sleep 2
kill  $SERVER_PID
sleep 3 
kill -KILL  $SERVER_PID