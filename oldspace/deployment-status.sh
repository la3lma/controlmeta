#!/bin/bash

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

(cd $DEPLOYDIR &&   eb status)

