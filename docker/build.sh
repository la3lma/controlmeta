#!/bin/sh

# Copy everything necessary to run controlmeta over to /controlmetra
# in anticipation of having it compiled into a docerfile.

# File in rootdir that contains list of all files that should go into
# the production fileset.
PRODUCTIONFILES="productionfiles.txt"

TARGETDIR="$(PWD)/controlmeta"

if [ -d "$TARGETDIR" ] ; then
    echo rm -rf "$TARGETDIR"
fi


# Copy the files we need
mkdir -p "$TARGETDIR"
PRODUCTIONDIRS=$(cat "../$PRODUCTIONFILES" | grep '/' | awk -F/ '{print $1}' | sort | uniq)
(cd "$TARGETDIR" && mkdir -p "$PRODUCTIONDIRS")
(cd .. ; cp $(cat "$PRODUCTIONFILES") "$TARGETDIR" )


# Then build the docker instance
docker build .

