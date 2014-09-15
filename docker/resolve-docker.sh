#!/bin/bash

# Build a docker instance from the docker instance that's available

DEFAULT_DOCKER_PORT="2375"

DOCKER="$(which docker)"
# Check that docker is installed
if [ -z "$DOCKER" ] ; then 
    echo "Did not find docker."
    if [ "$uname" = "Darwin" ] ; then
        echo "I see that you are running OSX, try installing it using brew install docker"
    fi
    exit 1
fi

uname=$(uname)


# Check that psgrep is installed
PSGREP="$(which psgrep)"
if [ -z "$PSGREP" ] ; then
   if [ "$uname" = "Darwin" ] ; then
        echo "Could not find psgrep."
        echo "I see that you are running OSX, you could try running 'brew install psgrep'"
        exit 1
   fi
fi


# Check that we have a docker host to connect to
if [ -z "$DOCKER_HOST" ] ; then

    if [ "$uname" = "Darwin" ] ; then
        BOOT2DOCKER="/usr/local/bin/boot2docker"
        echo "No DOCKER_HOST environment variable found, trying to find one, assuming docker runs on localhost"
        echo "I see that you are running OSX, you could try running  boot2docker start"
        if [ !  -x "$BOOT2DOCKER" ] ; then
            echo "I see that you have not installed boot2docker, you can get it here: http://boot2docker.io/"
            exit 1
        else
            if [ -z "$(psgrep boot2docker)" ] ; then
                echo "Could not find a running boot2docker, starting one."
                "$BOOT2DOCKER" start
                echo "Started boot2docker."
            else
                echo "Found a running boot2docker instance. We're assuming it uses the"
                echo "default port, and will set the DOCKER_HOST variable using that assumption"
            fi

            export DOCKER_HOST="tcp://$(boot2docker ip 2>/dev/null):$DEFAULT_DOCKER_PORT"
            if [ "tcp://:$DEFAULT_DOCKER_PORT" = "$DOCKER_HOST" ] ; then
                echo "Could not find a running boot2docker even after starting one, bailing out."
                echo 1
            fi
            echo "     DOCKER_HOST=$DOCKER_HOST"
        fi
    elif [ "$uname" = "Linux" ] ; then
        echo "I see that you are running Linux, I'll try to find docker on its unix socket (you didn't spec. DOCKER_HOST)"
    else
        echo "Unknown operating operating system $uname, cannot start docker. Please fix this script to amend"
        exit 1
    fi
else
    echo "Found environment variable DOCKER_HOST set to $DOCKER_HOST.  so we're using that."
fi

# Just making certain"
if [ -z "$DOCKER_HOST" ] ; then
    if [ "$uname" = "Linux" ] ; then
        echo ""
    else
        echo "Could not determine DOCKER_HOST, this is weird. You figure it out."
        exit 1
    fi
fi
