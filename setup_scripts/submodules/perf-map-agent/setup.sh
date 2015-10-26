#!/bin/bash

cd $PANYWHERE_HOME/submodules/perf-map-agent

# build
cmake .
make all -j$((`cat /proc/cpuinfo | grep processor | awk '{print $3}'| tail -1` + 1))


# export some enviromental variables
CURR_DIR=`pwd`
echo "export PERFMAPAGENT_HOME=$CURR_DIR" >> $PANYWHERE_HOME/setup_env_vars.sh
echo 'export PATH=$PATH:$PERFMAPAGENT_HOME' >> $PANYWHERE_HOME/setup_env_vars.sh

cd $PANYWHERE_HOME
