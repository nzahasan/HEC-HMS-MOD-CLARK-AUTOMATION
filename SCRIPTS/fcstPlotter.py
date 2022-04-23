#! /usr/bin/env python3
'''---------------------------------------------------------------
Creates 17 day (-1:fcstday:15) plumes 
plot for forecast output

Nazmul Ahasan
nzahasan@gmail.com
---------------------------------------------------------------'''

from datetime import datetime as dt
import rcCurve as rc
import sys, pylab as pl, numpy as np,pandas as pd

pl.style.use("fivethirtyeight") 

DANGER_LEVEL_WL = 19.5
DANGER_LEVEL_Q = rc.qbyRC(DANGER_LEVEL_WL)

def main():
	
	
	if len(sys.argv)>=4:
		
		fcstDate = sys.argv[1]
		csvDir = sys.argv[2]
		plotOutDir = sys.argv[3]
		
		if csvDir[-1] != '/':
			csvDir+='/'

		if plotOutDir[-1] != '/':
			plotOutDir+='/'

		try:
			if sys.argv[4]=="-s":
				showPlot=True
		except:
			showPlot=False
		
	else:
		print('fcstPlotter.py: Insufficient Argument\
			\n===================================== \
			\nPlease Provide the followings:- \
			\n\t# Forecast Date(yyyy-mm-dd) \
			\n\t# Model output CSV directory \
			\n\t# Plot output directory' \
			)
		sys.exit()
	
	dt.strptime(fcstDate,'%Y%m%d')

	fcstCsvDir=csvDir+fcstDate+"/"

	
	ens_dat=[]
	time = []

	# data format : row >> ens no , col >> day
	
	for ens_no in range(51):
		dischargeValues = []
		dischargeTimes = []
		
		try:
			ensFcstData = open(fcstCsvDir+fcstDate+".en-"+str(ens_no)+".csv").readlines()
		except:
			print('ERR: OUTPUT CSV FILE NOT FOUND FOR ENS '+str(ens_no))
			sys.exit()

		# if last line is empty or invalid
		if ensFcstData[-1] =="" or \
			len(ensFcstData[-1].split(','))<2:
			ensFcstData= ensFcstData[:-1]

		'''
			> why 17 day?
			16 day is ecmwf with 1st day copied back for missing cpc data
			so cpc start/common discharge is from last 17 day
			
			1 + 16
			^ 1st cpc data
			common point
		'''
		for line in ensFcstData[-17:]:
			dischargeValues.append(float(line.split(",")[1].replace("\n","")))
			dischargeTimes.append(line.split(",")[0])

		ens_dat.append(dischargeValues)
		
		if len(time)==0:
			for i in range(len(dischargeTimes)):
				time.append(dischargeTimes[i])
		else:
			if time != dischargeTimes:
				print("Time Mismatch between discharge time series, at ensemble no: "+str(ens_no))

	# numpy array conversion
	ens_dat = np.asarray(ens_dat,np.float32)
	
	for i in range(len(time)):
		# conversion to datetime
		time[i] = dt.strptime(time[i],"%d%b%Y %H:%M")


	quantile75 = np.zeros(17)
	median = np.zeros(17)
	quantile25 = np.zeros(17)


	for day in range(ens_dat.shape[1]):
		quantile75[day] = pd.Series(ens_dat[:,day]).quantile(0.75)
		median[day] = pd.Series(ens_dat[:,day]).quantile(0.5)
		quantile25[day] = pd.Series(ens_dat[:,day]).quantile(0.25)

	
	plot(fcstDate,time,ens_dat,quantile25,median,quantile75,plotOutDir,showPlot)
	

def plot(fcstDate,time,ens_dat,quantile25,median,quantile75,plotOutDir,showPlot):
	pl.figure(figsize=(22,11))

	# fill_plot
	for ensno in range(50):
		pl.fill_between(time,ens_dat[ensno],ens_dat[ensno+1],color='#0065ff',alpha=.05)

	# _quantiles & median
	pl.plot(time,quantile75,color='#001c46',linewidth=2.0,linestyle="--",alpha=0.6,label="75% Quantile")
	pl.plot(time,median,color='#001c46',linewidth=2.0,linestyle="-",alpha=0.75,label="Ensemble Median")
	pl.plot(time,quantile25,color='#001c46',linewidth=2.0,linestyle="--",alpha=0.6,label="25% Quantile")
	
	# danger level line
	pl.plot(time,[DANGER_LEVEL_Q]*len(time),color='red',linewidth=2,linestyle="--",alpha=0.5,label="Danger Level")

	# mark for forecast start time
	pl.scatter([time[2]],median[2],s=80,facecolors='none',linewidths=2,edgecolors='black')
	

	# tittle legend and plot style

	pl.title("15 Day Ensemble Discharge Forecast for Bahadurabad,As of "+fcstDate,\
			fontname="Noto Mono",size=18,y=1.06)

	pl.xticks(fontname='Freemono',size=16)
	pl.yticks(fontname='Freemono',size=16)
	pl.xlabel("Forecast Date",fontname='Freemono',size=20,labelpad=20)
	pl.ylabel("Discharge ($m^3/s$)",fontname="Freemono",size=20,labelpad=20)

	legend = pl.legend(bbox_to_anchor=(0.25, 1, 1, 0), loc=3,ncol=4, \
		mode=None, borderaxespad=0, fontsize=14)
	
	pl.setp(legend.texts,family="Noto Mono")

	if showPlot==True:
		print("Showing plot...")
		pl.show()
	else:
		pl.savefig(plotOutDir+fcstDate+".png")
		print("Saved forecast plot as, "+fcstDate+".png")

if __name__ == '__main__':
	main()


