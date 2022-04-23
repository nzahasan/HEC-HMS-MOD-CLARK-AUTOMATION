from pyramid.arima import auto_arima
import numpy as np

def predict(err_data):
		
	model = auto_arima(err_data,\
		error_action="ignore",\
		suppress_warnings=True,\
		stepwise=True,\
		method='nm')
	
	if sum(model.order) ==0:
		print('ARIMA//WARNING: ORDER IS (0,0,0) RETURNING nan')
		return np.array([np.nan]*15)


	predictedError = model.predict(n_periods=15)

	return predictedError

