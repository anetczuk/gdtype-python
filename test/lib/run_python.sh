#!/bin/bash

set -eu


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


LIB_DIR="$SCRIPT_DIR/../../src"


if [ -z ${PYTHONPATH+x} ]; then
    export PYTHONPATH="$LIB_DIR"
else 
    export PYTHONPATH="${PYTHONPATH}:$LIB_DIR"
fi


python3 $@
