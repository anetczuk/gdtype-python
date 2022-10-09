#!/bin/bash

set -eu


CFG_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_NAME=`basename "$0"`

CONFIG_PATH="$CFG_SCRIPT_DIR/../config.cfg"
##CONFIG_PATH="$SCRIPT_DIR/$SCRIPT_NAME.cfg"

if [ ! -f $CONFIG_PATH ]; then
cat > $CONFIG_PATH <<- EOM
##
## This is bash script containing configuration for merge.sh file
## Serves mostly as container for variables
##


## path Godot engine executable
ENGINE_V3_PATH=

ENGINE_V4_PATH=

EOM
fi


## load config file
source $CONFIG_PATH


read_engine_v3_path() {
    ## handle config variable
    if [[ ! "$ENGINE_V3_PATH" =~ ^/ ]]; then
        ## relative path -- add script path in front of
        ENGINE_V3_PATH="$SCRIPT_DIR/$ENGINE_V3_PATH"
    fi
    ENGINE_V3_PATH=$(readlink -m "$ENGINE_V3_PATH")
    
    if [ -z "$ENGINE_V3_PATH" ] || [ ! -f $ENGINE_V3_PATH ]; then
        echo "Given executable [$ENGINE_V3_PATH] not exists. Verify $CONFIG_PATH"
        exit 1
    fi
}

read_engine_v4_path() {
    ## handle config variable
    if [[ ! "$ENGINE_V4_PATH" =~ ^/ ]]; then
        ## relative path -- add script path in front of
        ENGINE_V4_PATH="$SCRIPT_DIR/$ENGINE_V4_PATH"
    fi
    ENGINE_V4_PATH=$(readlink -m "$ENGINE_V4_PATH")
    
    if [ -z "$ENGINE_V4_PATH" ] || [ ! -f $ENGINE_V4_PATH ]; then
        echo "Given executable [$ENGINE_V4_PATH] not exists. Verify $CONFIG_PATH"
        exit 1
    fi
}
