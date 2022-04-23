import pandas as pd 
import numpy as np
import rcCurve as rc
from datetime import datetime as dt
from datetime import timedelta as delt
import ARIMA,sys,os

import pylab as pl

import pylab as pl

def q_csv(wl_fname):
	

	# generate a qfile of bahadurabad data
	data = pd.read_csv(wl_fname)
	
	out_dat = pd.DataFrame()

	out_dat['Date'] = data['Date']
	out_dat['Flow'] = rc.qbyRC(data['WL'].values) 
	

	out_dat.to_csv('tst.csv')


def main():

	date_str = open('env_var/date','r').readlines()[0].replace('\n','')

	year = dt.strptime(date_str,'%Y%m%d').strftime('%Y')
	date_fmt2 = dt.strptime(date_str,'%Y%m%d').strftime('%Y-%m-%d')


	date = dt.strptime(date_str,'%Y%m%d')


	csv_in_dir = 'output/csv/ganges/'+date_str
	csv_out_dir = 'output/csv/ganges/c.'+date_str

	if csv_in_dir[-1]!='/':
		csv_in_dir+='/'

	if csv_out_dir[-1]!='/':
		csv_out_dir+='/'

	if not os.path.exists(csv_out_dir):
	    os.makedirs(csv_out_dir)

	'''
		check if last today & pre-day is available
		if not append
	'''

	wl_fname="qdat/GAN.WL."+year+".csv"
	wl_data = pd.read_csv(wl_fname)

	today = date.strftime('%d/%m/%Y')
	yesterday = (date-delt(days=1)).strftime('%d/%m/%Y')

	# today
	if max(wl_data['Date']==today):
		print('_')
	else:
		pass

	
	# today-1
	if max(wl_data['Date']==yesterday):
		print('_')
	else:
		pass
	
	'''
	 get last 60 day value
	 if not found place -9999
	'''

	start_date = date-delt(days=60)

	sim_dat = pd.read_csv(csv_in_dir+date_str+'.en-0.csv',names=['Date','Flow'])
	
	error = []
	dates = []

	for i in range(60):
		wl_date_str = (start_date+delt(days=i)).strftime('%d/%m/%Y')
		sim_q_date_str = (start_date+delt(days=i)).strftime('%d%b%Y 06:00')
		# print(wl_date_str)
		if max(wl_data['Date']==wl_date_str) and max(sim_dat['Date']==sim_q_date_str):
			
			
			
			obs_wl = wl_data.WL[wl_data['Date']==wl_date_str].values[0]
			obs_q = rc.qbyRC(obs_wl)

			sim_q = sim_dat.Flow[sim_dat['Date']==sim_q_date_str].values[0]

			_err = obs_q-sim_q
			# obs_q = rc

			dates.append(wl_date_str)
			error.append(_err)
		else:
			dates.append(wl_date_str)
			print('Missing value at '+wl_date_str)
			if len(error)==0:
				error.append(0)
			else:
				error.append((error[-1]+error[-2]+error[-3])/3)
			pass


	out_data = pd.DataFrame()
	out_data['Date'] = dates
	out_data['Err'] = error
	
	# get corrected error data from arima
	try:
		err = ARIMA.err_fcst(out_data)
	except:
		print('Failed to execute arima check data for wl')
		sys.exit()

	# read and wrie to ens output

	for ens_no in range(51):
		_ens_dat = pd.read_csv(csv_in_dir+date_str+'.en-'+str(ens_no)+'.csv',names=['Date','Flow'])
		
		_full_len_err = np.zeros(_ens_dat['Flow'].values.shape[0])
		
		_full_len_err[-17:-15] += out_data['Err'][-2:]
		_full_len_err[-15:] += err 
		_ens_dat['Flow'] += _full_len_err

		_ens_dat.to_csv(csv_out_dir+date_str+'.corr.en-'+str(ens_no)+'.csv', header=False,index=False)
		# break
	
if __name__ == '__main__':
	main() 
