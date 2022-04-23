from pyramid.arima import auto_arima

def predict(err_data):
		
	model = auto_arima(err_data,\
		error_action="ignore",\
		suppress_warnings=True,\
		stepwise=True,\
		method='nm')
	
	predictedError = model.predict(n_periods=15)

	return predictedError

