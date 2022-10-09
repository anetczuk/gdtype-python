#!/bin/bash

set -eu


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_NAME=`basename "$0"`


## load config file
source "$SCRIPT_DIR/lib/read_config.sh"

read_engine_v4_path


SCRIPT_PATH="$SCRIPT_DIR/lib/gd_tests_v4.gd"


cd $SCRIPT_DIR

$ENGINE_V4_PATH --headless --script $SCRIPT_PATH
