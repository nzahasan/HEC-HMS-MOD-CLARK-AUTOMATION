#! /usr/bin/env python3

""" -----------------------------------------

error correction scipt

Nazmul Ahasan Shawn	 
nzahasan@gmail.com

-----------------------------------------"""

from tensorflow import keras
import numpy as np,pandas as pd
import datetime as dt
import rcCurve as rc
import sys,os,pickle


def main():

	try:
		simDate = sys.argv[1]
		baseDir = sys.argv[2]
		if baseDir[-1]!='/':
			baseDir += '/'

		simYear = dt.datetime.strptime(simDate,"%Y%m%d").strftime('%Y')
	except:
		print('Insufficient argument\n ::Required Argument: simDate, baseDir')
		sys.exit()
	
	errorModFile = baseDir+'error_model/error.mod.'+simYear+'.h5'
	scalingParamDat = baseDir+'error_model/scaling.param.'+simYear+'.dat'
	
	csvInDir = baseDir+'OUTPUT/CSV/'
	wlDataDir = baseDir+'DATA/QDATA/'

	try:
		obsWLdata = pd.read_csv(wlDataDir+'BH.WL.'+str(simYear)+'.csv')
		simQdata = pd.read_csv(csvInDir+simDate+'/'+simDate+'.en-0.csv',names=['Date','Flow'])
	except:
		print('Simulation csv data not found')
		sys.exit()

	startDate=dt.datetime.strptime(simDate,"%Y%m%d")-dt.timedelta(days=30)
	error = np.zeros(30) 

	for i in range(1,31):
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
			if i-1!=0: error[i-1]=error[i-2]
	


	if not os.path.exists(scalingParamDat):
		print(scalingParamDat,'not found')
		
		if not os.path.exists(errorModFile):
			print(errorModFile,'not found')
			sys.exit()
		sys.exit()

	# scale error with training scaling parameter
	
	with open(scalingParamDat,'rb') as paramFile:
		scalingParam =pickle.load(paramFile)

	# print(scalingParam)

	scaledError = (error - scalingParam['min'])/(scalingParam['max']-scalingParam['min'])
	
	#: load trained error forecasting model
	
	errorModel = keras.models.load_model(errorModFile)

	fcstErr = errorModel.predict(scaledError.reshape( (-1,30,1) ) )

	fcstErr = fcstErr.reshape((15))
	invScaledFcstErr = (fcstErr * (scalingParam['max']-scalingParam['min']))+scalingParam['min']

	keras.backend.clear_session()
	#: ------------------------------------------------------------------------
	#: 	this is done due to pandas dosen't allow to set value in a slice
	#:	so only last 17 days is error corrected value in C.folder csv file
	#: ------------------------------------------------------------------------

	fullLenErr = np.zeros(simQdata.shape[0])
	fullLenErr[-17:-15] += error[-2:]
	fullLenErr[-15:] += invScaledFcstErr

	
	ecorrOutDir = csvInDir+'/C.'+simDate+'/'
	if not os.path.exists(ecorrOutDir):
		os.makedirs(ecorrOutDir)
	
	# save corrected forecast
	for ens_no in range(51):
		ens_dat = pd.read_csv(csvInDir+simDate+'/'+simDate+'.en-'+str(ens_no)+'.csv',names=['Date','Flow'])

		ens_dat['Flow'] = ens_dat['Flow'] + fullLenErr
		ens_dat.to_csv(ecorrOutDir+simDate+'.corr.en-'+str(ens_no)+'.csv',header=False,index=False)


if __name__ == '__main__':
	main()