#!/bin/sh

grep XXX $(find . -name '*.py' | grep -v "oldspace")
