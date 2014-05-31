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

# Nuke cruft
"${HOMEDIR}/clean.sh"

SUBDIRS="mediameta tasks ctlm .ebextensions"
# First clean up the deploydir
(cd $DEPLOYDIR && rm -f *.py $SUBDIRS)

TOPLEVEL_FILES_TO_DEPLOY="application.py config.py database.py create_database.py requirements.txt"

# Then copy relevant python scripts to the deploydir
cp $TOPLEVEL_FILES_TO_DEPLOY "$DEPLOYDIR"
cp -r $SUBDIRS "$DEPLOYDIR"

LAST_GIT_COMMIT=$(cd "$HOMEDIR" && git log | head -n 1 | awk '/commit/ {print $2}')

(cd $DEPLOYDIR && git add $TOPLEVEL_FILES_TO_DEPLOY $SUBDIRS)
(cd $DEPLOYDIR && git commit -a -m "New version, based in git commit $LAST_GIT_COMMIT")

# Finally push the new files to the application server
(cd $DEPLOYDIR && git aws.push && eb status)



