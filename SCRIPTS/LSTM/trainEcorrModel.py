#! /usr/bin/env python3

"""-------------------------------------------
	Trains error correction LSTM model 
	
	Nazmul Ahasan Shawn
	nzahasan@gmail.com

-------------------------------------------"""

from tensorflow import keras
import pylab as pl
import pandas as pd
import numpy as np
import datetime as dt
import pickle
import sys,os
pl.style.use('bmh')


class tsDatMk(object):
	def __init__(self,tsData,scaled=True):
		
		if type(tsData)==np.ndarray:
			self.tsDat = tsData
		else:
			print('ERROR: data needs to be a numpy array!')
		self.max = self.tsDat.max()
		self.min = self.tsDat.min()
		self.shape = self.tsDat.shape[0]
		if scaled == True:
			self.scaledTsDat = self.scale(self.tsDat)
		else:
			self.scaledTsDat = self.tsDat
	
	def formattedDat(self):
		# undefined behavior with numpy.empty
		
		XDATA = np.zeros((1,30,1))
		YDATA = np.zeros((1,15))
		
		for i in range(self.shape-(30+15-1)):
			XDATA = np.append( XDATA, self.scaledTsDat[i:i+30].reshape((1,30,1)) ,axis=0 )
			YDATA = np.append( YDATA, self.scaledTsDat[i+30:i+45].reshape(1,15) ,axis=0)
		
		
		return XDATA[1:,:,:],YDATA[1:,:]
	
	def scale(self,data):
		
		retDat = np.zeros(data.shape)
		
		retDat = (data-self.min) / (self.max - self.min)
		
		return retDat
	
	def inv_scale(self,data):
		retDat = np.zeros(data.shape)
		
		retDat = (data * (self.max - self.min) ) + self.min
		
		return retDat
	
	def get_scaling_param(self):
		
		return {'min':self.min,'max':self.max}





def main(num_epoch=1,eval_per=0.15,testPlots='y'):
	
	try:
		csvFile = sys.argv[1]
		modelOutDir = sys.argv[2]
		year = sys.argv[3]
	except:  
		print('Args: csvfile,outputdir,year,epoch,plot')
		sys.exit()

	if modelOutDir[-1]!="/": modelOutDir+='/'

	try: num_epoch = int(sys.argv[4])
	except: pass

	try: testPlots = (sys.argv[5]).lower()
	except: pass

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

	eval_samples = int(xDat.shape[0]*eval_per)

	xDatEval = xDat[0:eval_samples]
	xDatTrain = xDat[eval_samples:]

	yDatEval = yDat[0:eval_samples]
	yDatTrain = yDat[eval_samples:]

	scaling_param = data.get_scaling_param()

	with open(modelOutDir+'scaling.param.'+str(year)+'.dat','wb') as file:
		pickle.dump(scaling_param,file,pickle.HIGHEST_PROTOCOL)



	# :----------------: define & train model :----------------: #
	keras.backend.clear_session()
	model = keras.models.Sequential()
	model.add(keras.layers.LSTM(100,activation='sigmoid',input_shape=(30,1) ,go_backwards=False,return_sequences=False))
	model.add(keras.layers.Dense(15))
	model.compile(loss='mean_squared_error',optimizer='adam')
	trainHist = model.fit(xDatTrain,yDatTrain,epochs=num_epoch,batch_size=32,validation_split=0.2)
	model.save(modelOutDir+'error.mod.'+str(year)+'.h5')

	# :----------------: evaluate :----------------: # 

	evalLoss = model.evaluate(xDatEval,yDatEval,batch_size=32)
	print('Model Evaluation Loss: ',evalLoss)


	print('Generating plots...')
	# :----------------: fitting check :----------------: #
	valPlotDir = modelOutDir+'VAL-PLOT.'+year+'/'
	if not os.path.exists(valPlotDir):
		os.makedirs(valPlotDir)

	pl.figure(figsize=(12,6))
	pl.plot(trainHist.history['val_loss'],label='VAL')
	pl.plot(trainHist.history['loss'],label='Train')
	pl.title('Loss VS Epoch')
	pl.legend()
	pl.savefig(valPlotDir+'Loss_vs_Epoch.png')
	pl.close()

	# :----------------:  val plots  :----------------: #
	
	if testPlots == 'y':
		
		for _ in range(200):
			ind = np.random.randint(0,csvData.shape[0]-45)

			y = model.predict( xDat[ind,:,:].reshape(1,30,1) )
			pl.figure(figsize=(12,6))
			pl.plot(np.arange(30),data.inv_scale(xDat[ind,:,:].reshape(30)),alpha=0.4,label='FEED')
			pl.plot(np.arange(30,45),data.inv_scale(y.reshape(15)),alpha=0.4,label='FCST')
			pl.plot(np.arange(30,45),data.inv_scale(yDat[ind].reshape(15)),alpha=0.4,label='TRUE')
			pl.legend()
			pl.savefig(valPlotDir+str(ind)+'_plot.png')
			pl.close()
	# :----------------:  err plot  :----------------: #
	pl.figure(figsize=(12,6))
	pl.plot(csvData['ERR'],label='Model Error')
	pl.legend()
	pl.savefig(valPlotDir+'error_plot.png')
	pl.close()
	
	# clear tensorflow session 
	keras.backend.clear_session()

if __name__ == '__main__':
	main()