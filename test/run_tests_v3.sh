#!/bin/bash

set -eu


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_NAME=`basename "$0"`


## load config file
source "$SCRIPT_DIR/lib/read_config.sh"

read_engine_v3_path


SCRIPT_PATH="$SCRIPT_DIR/lib/v3/gd_tests_v3.gd"


cd $SCRIPT_DIR

$ENGINE_V3_PATH --headless --script --quit $SCRIPT_PATH
