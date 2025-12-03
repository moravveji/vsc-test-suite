#!/bin/bash -l

set -e
module load ReFrame/4.8.2-GCCcore-14.2.0
module load archspec/0.2.5-GCCcore-14.2.0
set +e

export RFM_CONFIG_FILES=$(dirname $0)/config_vsc.py
export RFM_CHECK_SEARCH_PATH=$(dirname $0)/tests
export RFM_OUTPUT_DIR=$VSC_SCRATCH/reframe
export RFM_PREFIX=$VSC_SCRATCH/reframe
export RFM_CHECK_SEARCH_RECURSIVE=true
export RFM_SAVE_LOG_FILES=true
export PYTHONPATH=$(dirname $0)/tests:$PYTHONPATH

reframe --run  "$@"
#rm $(dirname $0)/reframe.out $(dirname $0)/reframe.log
