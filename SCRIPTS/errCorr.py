#! /usr/bin/env python3

""" -----------------------------------------

Error correction scheme for model

Nazmul Ahasan Shawn	 
nzahasan@gmail.com

-----------------------------------------"""

import numpy as np,pandas as pd
import datetime as dt
import rcCurve as rc
import sys,os
import ARIMA


def main():

	if len(sys.argv)>=3:
		simDate = sys.argv[1]
		baseDir = sys.argv[2]
		if baseDir[-1]!='/':
			baseDir += '/'

		simYear = dt.datetime.strptime(simDate,"%Y%m%d").strftime('%Y')
	else:
		print('Insufficient argument\n ::Required Argument: Simulation date\n, Base Directory')
		sys.exit()
	
	csvInDir = baseDir+'OUTPUT/CSV/'
	wlDataDir = baseDir+'DATA/QDATA/'

	try:
		obsWLdata = pd.read_csv(wlDataDir+'BH.WL.'+str(simYear)+'.csv')
		simQdata = pd.read_csv(csvInDir+simDate+'/'+simDate+'.en-0.csv',names=['Date','Flow'])
	except:
		print('ERR: SIM OR WL CSV NOT FOUND!')
		sys.exit()

	startDate=dt.datetime.strptime(simDate,"%Y%m%d")-dt.timedelta(days=60)
	error = np.zeros(60) 

	# hints :
		# if its 20 jan and i want to feed 10 day data including today
		# then the data i will feed 11-20 jan

	for i in range(1,61):
		obsWLdate =  (startDate+dt.timedelta(days=i)).strftime('%d/%m/%Y')
		simQdate =  (startDate+dt.timedelta(days=i)).strftime('%d%b%Y 06:00')
		
		try:
			obsWL =  obsWLdata['WL'][ obsWLdata['Date'] == obsWLdate ].values[0]
			obsQ = rc.qbyRC(obsWL)
			simQ = simQdata['Flow'][ simQdata['Date'] == simQdate ].values[0]
			errQ = obsQ-simQ
			error[i-1]=errQ
		except:
			print("Missing data at date: ",obsWLdate)
			error[i-1]=np.nan
	
	# interpolate missing (nan) data
	error = pd.Series(error).interpolate(limit_direction='both').values

	try:
		fcstErr = ARIMA.predict(error)
	except:
		print('WARNING: Failed to execute ARIMA, Using forecast blending.')
		fcstErr = np.array([np.nan]*15)

	# in case ARIMA fails add stepwise blending blending
	if np.isnan(fcstErr.sum()) : 
		print('WARNING: ARIMA returned nan, Using forecast blending.')
		fcstErr = np.array([error[-1] ]*15)
	
	#: ------------------------------------------------------------------------
	#: 	this is done due to pandas dosen't allow to set value in a slice
	#:	so only last 17 days is error corrected value in C.folder's csv file's
	#: ------------------------------------------------------------------------

	fullLenErr = np.zeros(simQdata.shape[0])
	fullLenErr[-17:-15] += error[-2:]
	fullLenErr[-15:] += fcstErr

	
	ecorrOutDir = csvInDir+'/C.'+simDate+'/'
	if not os.path.exists(ecorrOutDir):
		os.makedirs(ecorrOutDir)
	
	# save corrected forecast
	for ens_no in range(51):
		try:
			ens_dat = pd.read_csv(csvInDir+simDate+'/'+simDate+'.en-'+str(ens_no)+'.csv',names=['Date','Flow'])
		except:
			print("ERROR: FAILED TO READ OUTPUT FOR ENS "+str(ens_no))

		# add error to simulation data
		ens_dat['Flow'] = ens_dat['Flow'] + fullLenErr
		ens_dat.to_csv(ecorrOutDir+simDate+'.corr.en-'+str(ens_no)+'.csv',header=False,index=False)


if __name__ == '__main__':
	main()