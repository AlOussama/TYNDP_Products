#!/usr/bin/env bash
set -eu
python -m unittest discover -v -p 'test*.py'
python pinned/test_freedom.py
