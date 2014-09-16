#!/bin/sh

# Copy everything necessary to run controlmeta over to /controlmetra
# in anticipation of having it compiled into a docerfile.

BUILD_HOME_DIR=$(dirname "$0")


# File in rootdir that contains list of all files that should go into
# the production fileset.
PRODUCTIONFILES="productionfiles.txt"

TARGETDIR="$(PWD)/controlmeta"

if [ -d "$TARGETDIR" ] ; then
    rm -rf "$TARGETDIR"
fi


# Copy the files we need
mkdir -p "$TARGETDIR"

for file in $(cat "../$PRODUCTIONFILES") ; do
    DIRNAME="$(dirname $file)"
    if [ -n "$DIRNAME" ] ; then
	mkdir -p "$TARGETDIR/$DIRNAME"
    fi
    cp "../$file" "$TARGETDIR/$file"
done


# get the DOCKER_HOST environment variable (or fail&exit if unsuccessfull)
. $BUILD_HOME_DIR/resolve-docker.sh

# Then build the docker instance
docker build --tag="controlmeta" .

