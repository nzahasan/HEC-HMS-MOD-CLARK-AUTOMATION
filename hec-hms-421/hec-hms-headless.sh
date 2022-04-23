# /usr/bin/env bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

PROG=hms.Hms

# set $JAVA_EXE  to the java runtime executable
JAVA_EXE=$DIR/java/bin/java

# ******************************************************************

HMS_HOME=$DIR

JAVA_LIB_PATH=$HMS_HOME
JAVA_LIB_OPT="-Djava.library.path=$JAVA_LIB_PATH"

PYHOME=.
PYOPTS="-Dpython.path=$JARS -Dpython.home=$PYHOME"

$JAVA_EXE -Djava.awt.headless=true -DMapPanel.NoVolatileImage=true -Xms32M -Xmx1024M $PYOPTS $JAVA_LIB_OPT -classpath $DIR/*:$DIR/ui:$DIR/lib/*:$DIR/lib/hec/* $PROG $*

