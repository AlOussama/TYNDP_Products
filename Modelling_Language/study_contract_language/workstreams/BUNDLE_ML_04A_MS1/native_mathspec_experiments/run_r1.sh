#!/usr/bin/env bash
set -eu
# Run inherited original suite without rewriting it. The system python must be capable.
python -m unittest discover -v -p 'test*.py'
