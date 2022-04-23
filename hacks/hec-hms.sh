#! /usr/bin/env bash

# Stock Jython interface dosent support sys argument
# a little workaround is to setting sys.argv value manually
# this shell scripts takes the python script then replaces it 
# with the passed sys argument -> saves in temp directory with 
# a random name -> executes the newly saved file finally deletes the file  
# &
# in script mode it looks for display which is un-necessary
# so added headless mode using `-Djava.awt.headless=true`

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

# ******************************************************************

if [[ "$1" == "-s" ]];then      
		
		# a hack to support sysarguments

		script_data="$(<$2)"
		
		python_args="import sys;sys.argv=['${2}'"

		for (( i = 3; i <= $#; i++ )); do
				python_args="${python_args},'${!i}'"

		done
		python_args="${python_args}]"
		
		script_data="${script_data//#__(import sys)__#/${python_args}}"

		randfname="/tmp/`cat /dev/urandom | tr -cd 'a-f0-9' | head -c 25`.${2}"

		echo "$script_data" > $randfname

		$JAVA_EXE -DMapPanel.NoVolatileImage=true -Djava.awt.headless=true -Xms32M -Xmx1024M $PYOPTS $JAVA_LIB_OPT -classpath $DIR/*:$DIR/ui:$DIR/lib/*:$DIR/lib/hec/* $PROG -s $randfname
		rm $randfname

else
		$JAVA_EXE -DMapPanel.NoVolatileImage=true -Xms32M -Xmx1024M $PYOPTS $JAVA_LIB_OPT -classpath $DIR/*:$DIR/ui:$DIR/lib/*:$DIR/lib/hec/* $PROG $*
fi

