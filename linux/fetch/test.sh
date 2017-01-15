#!/bin/bash
for test_py in `ls *test.py`; do
  python $test_py
done
