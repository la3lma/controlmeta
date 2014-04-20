#!/bin/sh
clear

PYTHON=/usr/bin/python
TESTS="test_empty_crud.py \
      test_media_and_meta_storage_directly.py \
      test_task_queue_storage.py \
      test_media_usecases.py \
      test_flask_task_manipulations.py "


for test in $TESTS ; do
  echo "======"
  echo "Running tests in ${test}"
  $PYTHON "tests/${test}"
done