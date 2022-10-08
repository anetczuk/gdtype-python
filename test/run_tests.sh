#!/bin/bash

set -eu


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_NAME=`basename "$0"`


## load config file
source "$SCRIPT_DIR/lib/read_config.sh"

read_engine_path


SCRIPT_PATH="$SCRIPT_DIR/lib/gd_tests.gd"


cd $SCRIPT_DIR

$ENGINE_PATH --headless --script $SCRIPT_PATH
