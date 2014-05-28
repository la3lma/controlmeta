#!/bin/bash

WD=$(dirname $0)

echo "================="
echo "UNIT TESTS"
echo
$WD/tests-unit.sh


echo "================="
echo "ACCEPTANCE TESTS"
echo
$WD/tests-acceptance.sh

