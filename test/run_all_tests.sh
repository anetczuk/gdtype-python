#!/bin/bash

set -eu


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


echo "Running unit tests:"
$SCRIPT_DIR/../src/testgdtype/runtests.py

echo ""
echo "Running GDScript tests:"
$SCRIPT_DIR/run_tests.sh
