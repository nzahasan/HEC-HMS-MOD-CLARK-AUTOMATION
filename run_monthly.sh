#! /usr/bin/env bash

#----------------------------------------
#	Monthly hindcast run script 		/
#---------------------------------------- 

mon=$1
year=$2
days=$((`cal $mon $year | awk 'NF {DAYS = $NF}; END {print DAYS}'`))

for ((day=1; day<=$days; day++)); do
	
	if (($day<10)); then
			dd="0${day}"
	else
			dd="${day}"
	fi

	echo "Processing ${year}${mon}${dd}..."
	bash run_model.sh ${year}${mon}${dd}
done
