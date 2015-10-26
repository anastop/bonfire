#!/bin/bash

cd $PANYWHERE_HOME/submodules/jfr-flame-graph

# build jfr-flame-graph
jmc_version=`echo $(basename $JAVA_HOME/lib/missioncontrol/plugins/com.jrockit.mc.common_*.jar) | sed 's/.*_\(.*\)\.jar/\1/'`
echo "JMC JAR version: $jmc_version"

jar1=com.jrockit.mc.common_$jmc_version.jar
mvn install:install-file -DlocalRepositoryPath=repo -DcreateChecksum=true -Dpackaging=jar -Dfile=$JAVA_HOME/lib/missioncontrol/plugins/$jar1 -DgroupId=com.jrockit.mc -DartifactId=com.jrockit.mc.common -Dversion=$jmc_version
echo "Installing JAR $jar"

jar2=com.jrockit.mc.flightrecorder_$jmc_version.jar
mvn install:install-file -DlocalRepositoryPath=repo -DcreateChecksum=true -Dpackaging=jar -Dfile=$JAVA_HOME/lib/missioncontrol/plugins/$jar2 -DgroupId=com.jrockit.mc -DartifactId=com.jrockit.mc.flightrecorder -Dversion=$jmc_version
echo "Installing JAR $jar"

sed -i -e "/<properties>/,/<\/properties>/ s|<jmc.version>.*</jmc.version>|<jmc.version>$jmc_version</jmc.version>|g" pom.xml

mvn clean install -U


CURR_PATH=`pwd`  
PAR_PATH=$(dirname `pwd`)


# export enviromental variables

JFR2FLAME_HOME=${CURR_PATH}
FLAMEGRAPH_HOME=${FLAMEGRAPH_HOME:=PAR_PATH/FlameGraph}

JFR2FLAME_BIN=$JFR2FLAME_HOME/bin/

echo "export JFR2FLAME_HOME=$JFR2FLAME_HOME" >> $PANYWHERE_HOME/setup_env_vars.sh
echo "export PATH=\$PATH:$JFR2FLAME_BIN" >> $PANYWHERE_HOME/setup_env_vars.sh

# generate wrapper scripts

mkdir -p bin

touch bin/call_jfrflamegraph || (rm bin/jcall_jfrflamegraph; touch bin/call_jfrflamegraph )
touch bin/jfr2flame || (rm bin/jfr2flame; touch bin/jfr2flame )

chmod +x bin/call_jfrflamegraph
chmod +x bin/jfr2flame

echo '#!/bin/bash' > bin/jfr2flame
echo '#!/bin/bash' > bin/call_jfrflamegraph

echo 'echo "Usage (prints every time): jfr2flame flightrecording.jfr flamegraph.svg"' >> bin/jfr2flame

echo 'TEMP="/tmp/stacktrace_samples.txt"' >> bin/jfr2flame
echo 'FILE=$1' >> bin/jfr2flame
echo 'FLAME_FILE=$2' >> bin/jfr2flame

echo 'java -jar $JFR2FLAME_HOME/target/org.wso2.jmc.flamegraph-0.0.1-SNAPSHOT.jar $*' >> bin/call_jfrflamegraph

echo '$JFR2FLAME_HOME/bin/call_jfrflamegraph -f $FILE -o $TEMP' >> bin/jfr2flame

echo 'cat $TEMP | $FLAMEGRAPH_HOME/flamegraph.pl > $FLAME_FILE' >> bin/jfr2flame

cd $PANYWHERE_HOME


