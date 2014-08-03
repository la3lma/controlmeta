#!/bin/sh
clear

PYTHON=/usr/bin/python


# Use the memory-only version of sqlite for
# unit tests.
export SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"

test="unit_test_suite.py"
echo "======"
echo "Running tests in ${test}"
$PYTHON "tests/${test}"

