#!/usr/bin/env bash

#:----------------------------------------------:
#: Asc2dssGrid.exe alternative for linux
#: by- Tom Evans(Thomas.A.Evans@usace.army.mil)
#:
#: place this script to hec-hms program directory
#: execute 'chmod +x asc2dssGrid.sh'
#:----------------------------------------------:

HMS_HOME=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

MAINCLASS="hec.heclib.grid.Asc2DssGrid"
APPNAME="asc2DssGrid"

JARDIR=${HMS_HOME}/lib/hec
CLASSPATH="${JARDIR}/heclib.jar"
CLASSPATH="${CLASSPATH}:${JARDIR}/hec.jar"
CLASSPATH="${CLASSPATH}:${JARDIR}/rma.jar"

LIBPATH=${HMS_HOME}
JAVA_EXE=${HMS_HOME}/java/bin/java

#:------------------------------------------------------:
#: Memory parameters									:
#:------------------------------------------------------:

VMPARAM="-ms32M -mx1024M"

eval ${JAVA_EXE} ${VMPARAM} -Djava.awt.headless=true -cp ${CLASSPATH} -Djava.library.path=${LIBPATH} ${MAINCLASS} $*
