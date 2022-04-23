#! /usr/bin/env bash

#: -------------------------------------------------------
#:	Automation script for the model	
#:  Run model for a specific day
#:
#:	usage: bash run-date.sh date(yyyymmdd)
#:	Nazmul Ahasan Shawn
#:	nzahasan@gmail.com
#:
#:	N.B. 	used yyyymmdd date format
#:
#: -------------------------------------------------------

# ctrl+c is not reliable for this case, use ctrl+z instead to terminate this script
trap '' 2

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
MODEL_DIR=${DIR}/brahmaputra_model
HMS_DIR=${DIR}/hec-hms-421

if (( $# !=1 )); then

	echo "Error: Minimum one argument required."
	echo "Example: run-date.sh date(yyyymmdd)"
	exit
fi

Date=$1
Year=`date +%Y -d "${Date}"`
CurrYear=`date +%Y`

#:-----------------------    [PREPARING DATA]    -----------------------:


if [[ $Year < $CurrYear ]]; then
	CPC_NC_NAME=precip.${Year}.nc
	CPC_NC_PATH=${DIR}/DATA/NC/CPC/YEARLY/${CPC_NC_NAME}

else
	CPC_NC_NAME=cpc.${Date}.nc
	CPC_NC_PATH=${DIR}/DATA/NC/CPC/DAILY/${CPC_NC_NAME}
fi


ECMWF_NC_NAME=R1E${Date}.crop.nc
ECMWF_NC_PATH=${DIR}/DATA/NC/ECMWF/${ECMWF_NC_NAME}


# [download data]

if [ ! -f ${CPC_NC_PATH} ]; then
	echo "Downloading CPC data..."

	wget ftp://ftp.cdc.noaa.gov/Datasets/cpc_global_precip/precip.${Year}.nc -q --show-progress -O ${CPC_NC_PATH}
	
	
	if [ $? -ne 0 ]; then
		echo "Failed to download CPC data."
		exit
	fi
fi

if [ ! -f ${ECMWF_NC_PATH} ]; then
	echo "Downloading ECMWF data..."
	wget http://www.rimes.int/services/EPS/R1E${Date}.crop.nc -q --show-progress -O ${ECMWF_NC_PATH}

	if [ $? -ne 0 ]; then
		echo "Failed to download ECMWF precipitation forecast."
		exit
	fi
fi


# [create some directory]

CPC_RAW_RASTER_DIR=${DIR}/DATA/RAW-RASTER/CPC/${Year}
ECMWF_RAW_RASTER_DIR=${DIR}/DATA/RAW-RASTER/ECMWF/${Date}
CPC_SHG_DIR=${DIR}/DATA/SHG/CPC/${Year}
ECMWF_SHG_DIR=${DIR}/DATA/SHG/ECMWF/${Date}
CPC_EC_DSS_DIR=${DIR}/DATA/DSS/CPC-ECMWF/${Date}



mkdir -p $CPC_RAW_RASTER_DIR $ECMWF_RAW_RASTER_DIR $CPC_SHG_DIR $ECMWF_SHG_DIR $CPC_EC_DSS_DIR

#: extract cpc data
python3 ${DIR}/SCRIPTS/cpcNc2asc.py ${CPC_NC_PATH} ${CPC_RAW_RASTER_DIR}


#: extract ecmwf data
python3 ${DIR}/SCRIPTS/ecmwfNc2asc.py ${ECMWF_NC_PATH} $ECMWF_RAW_RASTER_DIR ${Date}

#: convert cpc data to shg grid
python3 ${DIR}/SCRIPTS/toSHG.py ${CPC_RAW_RASTER_DIR} $CPC_SHG_DIR ${DIR}/prj

#: create a dss with cpc data only
CPC_DSS=${CPC_EC_DSS_DIR}/${Date}-CPC.dss

python3 ${DIR}/SCRIPTS/insert2dss-utc06.py ${HMS_DIR}/asc2dssGrid.sh $CPC_DSS $CPC_SHG_DIR


#: convert ecmwf data to shg grid and enter data to dss

for ens_no in {0..50}; do
	
	#: converting ecdata to shg
	mkdir -p ${ECMWF_SHG_DIR}/EN-${ens_no}
	
	python3 ${DIR}/SCRIPTS/toSHG.py ${ECMWF_RAW_RASTER_DIR}/EN-${ens_no} ${ECMWF_SHG_DIR}/EN-${ens_no}/ ${DIR}/prj
	
	#: copy cpc dss for ensemble forecast entry
	ENS_DSS=${CPC_EC_DSS_DIR}/${Date}-CPC-EC-EN-${ens_no}.dss
	cp $CPC_DSS $ENS_DSS

	#:------------------------------------------------------------------------------------
	# fill 1 day gap with previous same ensemble data(check this gap stays same or not)
	# if previous 1 day is not available insert first day ecmwf data ;)
	#:------------------------------------------------------------------------------------

	D_minus1_CPC=${DIR}/DATA/SHG/CPC/${Year}/`date +%Y%m%d -d "${Date} -1 day"`.asc

	if [ ! -f $D_minus1_CPC ]; then

		echo 'Filling gap of CPC data...'
		
		D_minus1_ECMWF=${DIR}/DATA/SHG/ECMWF/`date +%Y%m%d -d "${Date} -1 day"`/EN-${ens_no}/`date +%Y%m%d -d "${Date} -1 day"`.en-${ens_no}.asc
		
		if [ ! -f $D_minus1_ECMWF ]; then
			python3 ${DIR}/SCRIPTS/insert2dssSingle.py ${HMS_DIR}/asc2dssGrid.sh $ENS_DSS ${ECMWF_SHG_DIR}/EN-${ens_no}/${Date}.en-${ens_no}.asc `date +%Y%m%d -d "${Date} -1 day"`	
		else
			python3 ${DIR}/SCRIPTS/insert2dssSingle.py ${HMS_DIR}/asc2dssGrid.sh $ENS_DSS $D_minus1_ECMWF `date +%Y-%m-%d -d "${Date} -1 day"`
		fi

	fi
	
	#: enter ecmwf data
	python3 ${DIR}/SCRIPTS/insert2dss-utc06.py ${HMS_DIR}/asc2dssGrid.sh $ENS_DSS ${ECMWF_SHG_DIR}/EN-${ens_no}/

done	


#: end data processing



#:-----------------------    [RUNNING MODEL]    -----------------------:

#: write forecast run control date range

ctlStartDate="2 January ${Year}"
ctlEndDate="`date +%d' '%B' '%Y -d "${Date} +15 day"`"

echo 'Writing ctl file for run from '$ctlStartDate' to '$ctlEndDate'...'

ctlFile="$(<${DIR}/res/FORECAST_CTL.control.#)"
ctlFile="${ctlFile//<:_start-date_:>/${ctlStartDate}}"
ctlFile="${ctlFile//<:_end-date_:>/${ctlEndDate}}"

echo "$ctlFile">${MODEL_DIR}/FORECAST_CTL.control

#: write observed dicharge dss path in gauge file

dischargeDssPath="${DIR}/DATA/DSS/DISCHARGE/Discharge.dss"
gaugeFile="$(<${DIR}/res/BRAHMA_MOD_CLARK.gage.#)"
gaugeFile="${gaugeFile//<:_discharge-dss-path_:>/${dischargeDssPath}}"

echo "$gaugeFile">${MODEL_DIR}/BRAHMA_MOD_CLARK.gage

#: write grid ctl file date range @ ##>#

startDateRange="01JAN${year}:0600/02JAN${Year}:0600"
gridFIle="$(<${DIR}/res/BRAHMA_MOD_CLARK.grid.##)"
gridFIle="${gridFIle//<:_dss-start-path-date-range_:>/${startDateRange}}"

echo "$gridFIle">${DIR}/res/BRAHMA_MOD_CLARK.grid.#

#: Write runModel.py
runModel="$(<${DIR}/res/runModel.py.#)"
runModel="${runModel//<:_date_:>/${Date}}"
runModel="${runModel//<:_base-dir_:>/${DIR}}"
runModel="${runModel//<:_model-dir_:>/${MODEL_DIR}/}"

#: ^^ if tailing `/` is not provided, project dosent close in next run, be careful! ^^

echo "$runModel">${DIR}/SCRIPTS/runModel.py

#: now run the model:
#: - first delete Forecast_Run.dss__
#: - cause it keeps the forward run data

rm ${MODEL_DIR}/FORECAST.dss ${MODEL_DIR}/FORECAST.dsc


bash ${HMS_DIR}/hec-hms-headless.sh -s ${DIR}/SCRIPTS/runModel.py

#: add base-flow to output

addBf="$(<${DIR}/res/addBaseFlow.py.#)"
addBf="${addBf//<:_date_:>/${Date}}"
addBf="${addBf//<:_base-dir_:>/${DIR}}"

echo "$addBf">${DIR}/SCRIPTS/addBaseFlow.py

bash ${HMS_DIR}/hec-hms-headless.sh -s ${DIR}/SCRIPTS/addBaseFlow.py


#:-----------------------    [MODEL OUTPUT]    -----------------------:

#: extract output as csv

OUT_CSV_DIR=${DIR}/OUTPUT/CSV/$Date
mkdir -p $OUT_CSV_DIR

dssPath="${DIR}/OUTPUT/DSS/${Date}.dss"

outAsCSV="$(<${DIR}/res/outputAsCSV.py.#)"
outAsCSV="${outAsCSV//<:_date_:>/${Date}}"
outAsCSV="${outAsCSV//<:_dss-file-path_:>/${dssPath}}"
outAsCSV="${outAsCSV//<:_output-csv-path_:>/${OUT_CSV_DIR}}"


echo "$outAsCSV">${DIR}/SCRIPTS/outputAsCSV.py


bash ${HMS_DIR}/hec-hms-headless.sh -s ${DIR}/SCRIPTS/outputAsCSV.py

#: Download WL from ffwc website

python3 ${DIR}/SCRIPTS/ffwcWL.py $Date $DIR

#: Error Correction with LSTM

python3 ${DIR}/SCRIPTS/errCorr.py $Date $DIR

#: create forecast plot

python3 ${DIR}/SCRIPTS/fcstPlotter.py $Date ${DIR}/OUTPUT/CSV/ ${DIR}/OUTPUT/PLOTS/

#: plot with error corrected forecast data
python3 ${DIR}/SCRIPTS/fcstPlotter.c.py $Date ${DIR}/OUTPUT/CSV/ ${DIR}/OUTPUT/PLOTS/

trap 2 

#_(end)_