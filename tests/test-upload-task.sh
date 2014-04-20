#!/bin/bash

# Upload a simple task to the service running in EC2


# A crufty way to deploy using amazon's standard ways of doing things.
# It feels clunky, so probably it is.

HOMEDIR=$(dirname  "$0")
DEPLOYDIR="$HOMEDIR/../controlmeta.aws"
UPLOADPY="$HOMEDIR/test-upload-task.py"

if [  -z "$(type eb)" ]  ; then
  echo "No 'eb' utility found in PATH variable, bailing out"
  exit 1
fi

if [ !  -d "$DEPLOYDIR" ] ; then
  echo "Could not find  deployment directory ,$DEPLOYDIR', bailing our"
  exit 1
fi

if [ ! -f "$UPLOADPY" ] ; then
  echo "Could not find upload-script '$UPLOADPY', bailing out"
  exit 1
fi

if [ ! -x "$UPLOADPY" ] ; then
  echo "upload-script '$UPLOADPY' exists but isn't executable, bailing out"
  exit 1
fi


URL_STEM="$((cd "$DEPLOYDIR" && eb status) | awk -F: '/^URL/ {print $2}' |  sed -e 's/^[ \t]*//')"

if [ -z "$URL_STEM" ] ; then
    echo "No URL stem found, bailing out"
    exit 1
fi

BASE_URL="http://${URL_STEM}/"



"$UPLOADPY" $BASE_URL




