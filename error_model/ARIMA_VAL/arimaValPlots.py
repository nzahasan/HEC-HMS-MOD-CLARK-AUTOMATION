#! /usr/bin/env python3

"""-------------------------------------------
	Checking performace of ARIMA 
	
	Nazmul Ahasan Shawn
	nzahasan@gmail.com

-------------------------------------------"""


import pylab as pl
import pandas as pd
import numpy as np
import datetime as dt
import sys,os
import ARIMA
pl.style.use('bmh')


class tsDatMk(object):
	def __init__(self,tsData,scaled=False):
		
		if type(tsData)==np.ndarray:
			self.tsDat = tsData
		else:
			print('ERROR: data needs to be a numpy array!')
		self.max = self.tsDat.max()
		self.min = self.tsDat.min()
		self.shape = self.tsDat.shape[0]
		
	
	def formattedDat(self):
		# undefined behavior with numpy.empty
		
		XDATA = np.zeros((1,60))
		YDATA = np.zeros((1,15))
		
		for i in range(self.shape-(60+15-1)):
			XDATA = np.append( XDATA, self.tsDat[i:i+60].reshape((1,60)) ,axis=0 )
			YDATA = np.append( YDATA, self.tsDat[i+60:i+75].reshape(1,15) ,axis=0)
		
		
		return XDATA[1:,:],YDATA[1:,:]
	

def main(num_epoch=1,eval_per=0.15,testPlots='y'):
	
	try:
		csvFile = sys.argv[1]
		year = sys.argv[2]
		
	except:  
		print('Args: csvfile,year')
		sys.exit()
	
	try:
		csvData = pd.read_csv(csvFile,parse_dates=['DATE'])
	except: 
		print('E: cant read csv file, is  filename okay?')
		sys.exit()

	try:
		csvData['ERR'] = csvData['OBS']-csvData['SIM']
		error = csvData['ERR'].values
		csvData.set_index('DATE')
	except:
		print('E: is the data field okay? there should be DATE, OBS and SIM column!')
		sys.exit()

	data = tsDatMk(error)

	xDat,yDat = data.formattedDat()
	
	
	print('Generating plots...')
	
	valPlotDir = 'VAL-PLOT-ARIMA.'+year+'/'
	if not os.path.exists(valPlotDir):
		os.makedirs(valPlotDir)

	
	# :----------------:  val plots  :----------------: #
	
	if testPlots == 'y':
		
		for _ in range(200):
			ind = np.random.randint(0,csvData.shape[0]-75)

			forecastErr = ARIMA.predict( xDat[ind,:].reshape(60) )
			pl.figure(figsize=(12,6))
			pl.plot(np.arange(60),xDat[ind,:].reshape(60),alpha=0.4,label='FEED')
			pl.plot(np.arange(60,75),forecastErr.reshape(15),alpha=0.4,label='FCST')
			pl.plot(np.arange(60,75),yDat[ind].reshape(15),alpha=0.4,label='TRUE')
			pl.legend()
			pl.savefig(valPlotDir+str(ind)+'_plot.png')
			pl.close()
	# :----------------:  err plot  :----------------: #
	pl.figure(figsize=(12,6))
	pl.plot(csvData['ERR'],label='Model Error')
	pl.legend()
	pl.savefig(valPlotDir+'error_plot.png')
	pl.close()
	

if __name__ == '__main__':
	main()