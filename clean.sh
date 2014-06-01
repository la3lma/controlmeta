#!/bin/bash

echo "Clearing old *.pyc and *~ files"

rm -rf $(find . -name '*~')
rm -rf $(find . -name '*.pyc')

echo "done."