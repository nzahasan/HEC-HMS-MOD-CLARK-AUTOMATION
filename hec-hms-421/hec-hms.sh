#/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

PROG=hms.Hms

# set $JAVA_EXE  to the java runtime executable
JAVA_EXE=$DIR/java/bin/java
# ******************************************************************
if [ "$DISPLAY" = "" ]
then
        XvfbRunning=`ps -ef | grep Xvfb | grep -v grep | wc -l | sed -e "s/ //g"`
        if [ $XvfbRunning -gt 0 ]
        then
                export DISPLAY=":1.0"
                printf "\nWARNING : Using virtual display - no graphics will be visible.\n\n"
        else
                printf "\nWARNING : Virtual display server is not running."
                printf "\n          Set DISPLAY variable or start Xvfb.\n\n"
                return -1
        fi
fi
# ******************************************************************

HMS_HOME=$DIR

JAVA_LIB_PATH=$HMS_HOME
JAVA_LIB_OPT="-Djava.library.path=$JAVA_LIB_PATH"

PYHOME=.
PYOPTS="-Dpython.path=$JARS -Dpython.home=$PYHOME"

$JAVA_EXE -DMapPanel.NoVolatileImage=true -Xms32M -Xmx1024M $PYOPTS $JAVA_LIB_OPT -classpath $DIR/*:$DIR/ui:$DIR/lib/*:$DIR/lib/hec/* $PROG $*

