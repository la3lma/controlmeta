#!/bin/bash

# Test regression with a full stack, using wire-protocols

BASEDIR=$(dirname $0)

TMPDIR=$BASEDIR/tmp

if [ ! -d "$TMPDIRR" ] ;  then
    mkdir -p "$TMPDIR"
fi


# The base url is the url the application is running at.
# it is necessary to send in as parameter, since I don't yet
# know how to pick it up from within application.py.

START_SERVER=""
BASE_URL="$1"
if [ -z "$BASE_URL" ] ; then
    BASE_URL="http://localhost:5000/"
    START_SERVER="yes"
fi

echo "Using BASE_URL = $BASE_URL"

PYTHON=/usr/bin/python
# Start the service

if [ ! -z "$START_SERVER" ] ; then 

    # Instruct the application where to find its datase instance.
    # We'll use an sqlite instance based on a local file.

    export SQLALCHEMY_DATABASE_URI="sqlite:///testdb.db"

    STDOUT="${TMPDIR}/server.out"
    STDERR="${TMPDIR}/server.err"
    
    $PYTHON application.py  "$BASE_URL" > "$STDOUT" 2> "$STDERR" &
    SERVER_PID=$!
    
    # Busy wait until server is up
    PHRASE_TO_WAIT_FOR="Restarting with reloader"
    
    echo -n "Waiting for server .."
    while  grep -s "PHRASE_TO_WAIT_FOR" "$STDERR" ; do
	echo -n "."
	sleep 0.5
    done
    
    sleep 1

    echo
    echo "Server running, starting tests."
fi

TESTS="test-upload-media.py test-upload-task.py"

SUCCESS_OR_FAILURE="succeeded"

for test in $TESTS ; do 
   TESTFILE="tests/$test"
   STDOUT="${TMPDIR}/${test}.out"
   STDERR="${TMPDIR}/${test}.err"
   
   if [ ! -f "$TESTFILE" ] ; then
       echo "ERROR: Could not find testfile $TESTFILE, aborting acceptance testing."
       SUCCESS_OR_FAILURE="failed"
       break
   fi

   # Nuke old testdb if present.
   (cd "$BASEDIR" && $PYTHON create_database.py)

   echo -n "Running test $test, stdout/err to files in $TMPDIR ..."
   $PYTHON "${TESTFILE}" "$BASE_URL" > "$STDOUT" 2> "$STDERR"
   EXIT_CODE=$?
   if  [ "$EXIT_CODE" != "0" ] ; then
       echo ""
       echo "ERROR: The test $test failed.  Aborting acceptance testing."
       echo "  See stderr from the test in $STDERR"
       echo "  See stdout from the test in $STDOUT"
       SUCCESS_OR_FAILURE="failed"
       break
   else
       echo "  Success."
   fi
done


echo "Acceptance tests run against the server at $BASE_URL ${SUCCESS_OR_FAILURE}."

if [ ! -z "$START_SERVER" ] ; then 
   ## XXX
   ## This should be optional, if we're running against a server running somewhere
   ## else, but for now it's ok.

   # Finally shut down the server
    sleep 2
    kill  $SERVER_PID
    for  pid in $(pgrep -P "$SERVER_PID" ) ; do 
	kill $pid
    done
    
    if pgrep "$SERVER_PID" ; then 
	kill -KILL  $SERVER_PID
    fi
    for pid in $(pgrep -P $SERVER_PID) ; do 
	kill -KILL $pid
    done
fi


# Finally return a sane return value    
if [ "$SUCCESS_OR_FAILURE" = "succeeded" ] ; then
    exit 0
else
    exit 1
fi

