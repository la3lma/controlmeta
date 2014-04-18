#!/bin/sh

# A crufty way to deploy using amazon's standard ways of doing things.
# It feels clunky, so probably it is.

HOMEDIR=$(dirname  "$0")
DEPLOYDIR="$HOMEDIR/../controlmeta.aws"

if [  -z "$(type eb)" ]  ; then
  echo "No 'eb' utility found in PATH variable, bailing out"
  exit 1
fi

if [ !  -d "$DEPLOYDIR" ] ; then
  echo "Could not find  deployment directory ,$DEPLOYDIR', bailing our"
  exit 1
fi
# First clean up the deploydir
(cd $DEPLOYDIR && rm -f *.py)

# Then copy all python scripts that are not for testing to the deploydir
cp $(ls $HOMEDIR/*.py | grep -v test) "$DEPLOYDIR"

(cd $DEPLOYDIR && git commit -a -m "New version")

# Finally push the new files to the application server
(cd $DEPLOYDIR && git aws.push && eb status)



