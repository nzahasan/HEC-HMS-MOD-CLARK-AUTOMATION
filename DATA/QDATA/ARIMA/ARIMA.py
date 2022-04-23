from pyramid.arima import auto_arima
import pandas as pd
import numpy as np,sys
from datetime import datetime as dt

def err_fcst(err_data):
	
	error=err_data['Err'].values.T
	# error = error.values
	
	model = auto_arima(error,\
		error_action="ignore",\
		suppress_warnings=True,\
		method='nm')


	_err_prediction = model.predict(n_periods=15)

	return _err_prediction

