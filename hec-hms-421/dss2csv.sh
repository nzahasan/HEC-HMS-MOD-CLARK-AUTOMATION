#! /usr/bin/env bash 
#:------------------------------------------------------------
#: place dss2csv.sh and d2c file in hec-hms root dir
#: usage: dss2csv.sh dssfile-path path-name output.csv-path
#:
#: Nazmul Ahasan
#: nzahasan@gmail.com
#:------------------------------------------------------------

if (($# < 3)) ; then
	echo "Example: dss2csv.sh DSS_Path Data_Path Output_csv"
	exit 1
fi


DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
HMS_EX=${DIR}/hec-hms.sh

# [get sys args]

DSSFILE=$1
DSSPATH=$2
CSVFILE=$3

# [gen a rand file name]

tmpFile=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)
tmpFile=${DIR}/${tmpFile}

# [replace parseable tags with sys args]
script="$(<${DIR}/d2c)"
script="${script//<:_dss-file-path_:>/$DSSFILE}"
script="${script//<:_data-path_:>/$DSSPATH}"
script="${script//<:_csv-path_:>/$CSVFILE}"

echo "$script">$tmpFile

# [execute scripts]
bash ${HMS_EX} -s $tmpFile
rm $tmpFile