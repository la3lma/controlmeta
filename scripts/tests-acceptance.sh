#!/bin/bash

# Test regression with a full stack, using wire-protocols

BASEDIR=$(dirname $0)

TMPDIR=$BASEDIR/tmp

if [ ! -d "$TMPDIRR" ] ;  then
    mkdir -p "$TMPDIR"
fi


export USERNAME="dummy-user@acceptance-tests.org"
export PASSWORD="VeRySeCReTpAsSw0Rd"

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

    SERVER_STDOUT="${TMPDIR}/server.out"
    SERVER_STDERR="${TMPDIR}/server.err"
    
    $PYTHON application.py  "$BASE_URL" > "$SERVER_STDOUT" 2> "$SERVER_STDERR" &
    SERVER_PID=$!
    
    # Busy wait until server is up
    PHRASE_TO_WAIT_FOR="Restarting with reloader"
    
    echo -n "Waiting for server .."
    while  grep -s "PHRASE_TO_WAIT_FOR" "$SERVER_STDERR" ; do
	echo -n "."
	sleep 0.5
    done
    
    sleep 1

    echo
    echo "Server running, starting tests."
fi


# Very useful URL to reset the user database
RESET_URL="${BASE_URL}reset"

# Very useful URL to reset the user database
USERS_URL="${BASE_URL}users"



TESTS="test-availability-of-user.py test-upload-media.py test-upload-task.py test-image-processing-roundtrip.py"

SUCCESS_OR_FAILURE="succeeded"


BASEDIR=$(dirname $(cd  $(dirname "$0") ; pwd -P))
CREATE_DATABASE_SCRIPT="$BASEDIR/scripts/create_database.py"

if [ ! -f "$CREATE_DATABASE_SCRIPT" ] ; then
   echo "Could not find database creation script $CREATE_DATABASE_SCRIPT"
   exit 1
fi



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
   (cd "$BASEDIR" && $PYTHON "$CREATE_DATABASE_SCRIPT")

   # Reset the user database (so that we can log in)
   curl "$RESET_URL" > /dev/null 2>&1

   # On osx, open the users URL just to see if it's ok.  Very
   # useful for debuggingg, so I'll keep it here for a while
   # open "$USERS_URL"

   echo -n "Running test $test, stdout/err to files in $TMPDIR ..."
   $PYTHON "${TESTFILE}" "$BASE_URL" > "$STDOUT" 2> "$STDERR"

   EXIT_CODE=$?
   if  [ "$EXIT_CODE" != "0" ] ; then
       echo ""
       echo "ERROR: The test $test failed (exit code = $EXIT_CODE).  Aborting acceptance testing."
       echo "  See stderr from the test in $STDERR"
       echo "  See stdout from the test in $STDOUT"
       SUCCESS_OR_FAILURE="failed"
   fi


   if [ "$SUCCESS_OR_FAILURE" = "failed" ] ; then
       break
   else
       echo "  Success."
   fi
   
done


echo "Acceptance tests run against the server at $BASE_URL ${SUCCESS_OR_FAILURE}."

if [ ! -z "$START_SERVER" ] ; then 

   # Finally shut down the server (if one is running)
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

