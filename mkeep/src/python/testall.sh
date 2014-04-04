#!/bin/sh
clear

PYTHON=/usr/bin/python
TESTS="empty_crud_tests.py \
      test_media_and_meta_storage_directly.py \
      media_usecases_test.py"


for test in $TESTS ; do
  echo "======"
  echo "Running tests in ${test}"
  $PYTHON "${test}"
done