#!/bin/bash

##
## Script installs copy of package into Python's user directory.
##

set -eu

## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


pip3 install --user "$SCRIPT_DIR" 
