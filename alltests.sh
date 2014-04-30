#!/bin/bash

WD=$(dirname $0)
# First we run all unit tests
$WD/tests-unit.sh

# Then we run the acceptance tests
$WD/tests-acceptance.sh

