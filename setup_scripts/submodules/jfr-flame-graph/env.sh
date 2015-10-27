#!/bin/bash


cd $BONFIRE_HOME/submodules/jfr-flame-graph

CURR_PATH=`pwd`  
PAR_PATH=$(dirname `pwd`)


# export enviromental variables

JFR2FLAME_HOME=${CURR_PATH}
FLAMEGRAPH_HOME=${FLAMEGRAPH_HOME:=PAR_PATH/FlameGraph}

JFR2FLAME_BIN=$JFR2FLAME_HOME/bin/

echo "export JFR2FLAME_HOME=$JFR2FLAME_HOME" >> $BONFIRE_HOME/setup_env_vars.sh
echo "export PATH=\$PATH:$JFR2FLAME_BIN" >> $BONFIRE_HOME/setup_env_vars.sh


cd $BONFIRE_HOME
