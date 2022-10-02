#!/bin/bash

set -eu


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_NAME=`basename "$0"`


## load config file
source "$SCRIPT_DIR/read_config.sh"

read_engine_path


SCRIPT_PATH="$SCRIPT_DIR/sample.gd"

$ENGINE_PATH --headless --script $SCRIPT_PATH
