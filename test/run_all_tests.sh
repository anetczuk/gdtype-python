#!/bin/bash

set -eu


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


echo "Running unit tests:"
$SCRIPT_DIR/../src/testgdtype/runtests.py

echo ""
echo "Running GDScript v3 tests:"
$SCRIPT_DIR/run_tests_v3.sh

echo ""
echo "Running GDScript v4 tests:"
$SCRIPT_DIR/run_tests_v4.sh
