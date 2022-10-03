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
ENGINE_PATH=

EOM
fi


## load config file
source $CONFIG_PATH


read_engine_path() {
    ## handle config variable
    if [[ ! "$ENGINE_PATH" =~ ^/ ]]; then
        ## relative path -- add script path in front of
        ENGINE_PATH="$SCRIPT_DIR/$ENGINE_PATH"
    fi
    ENGINE_PATH=$(readlink -m "$ENGINE_PATH")
    
    if [ -z "$ENGINE_PATH" ] || [ ! -f $ENGINE_PATH ]; then
        echo "Given executable [$ENGINE_PATH] not exists. Verify $CONFIG_PATH"
        exit 1
    fi
}
