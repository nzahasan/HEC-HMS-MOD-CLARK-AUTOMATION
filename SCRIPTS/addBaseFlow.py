'''-------------------------------------------------------
Add's baseflow to discharge output of Bahadurabad

Filter with 'OUTPUT+BF' to see all baseflow added data

Nazmul Ahasan Shawn
nzahasan@gmail.com
-------------------------------------------------------'''

from hec.script import *
from hec.heclib.dss import *
from hec.heclib.util import *
from hec.io import *
import java,time


def main():
	
	DATE = '20180718'

	baseDir = '/home/nazmul/ModelWOrk/MOD-CLARK'

	if baseDir[-1]!='/':
		baseDir+='/'

	#----------------- [Load Baseflow Data] -----------------#
	leapBaseFlow = open(baseDir+'baseflow/bh.bf.366','r').readlines()
	nonLeapBaseFlow = open(baseDir+'baseflow/bh.bf.365','r').readlines()

	for i in range(len(leapBaseFlow)):
		leapBaseFlow[i] = float(leapBaseFlow[i]\
			.replace('\r','').replace('\n','').replace(' ',''))

	for i in range(len(nonLeapBaseFlow)):
		nonLeapBaseFlow[i] = float(nonLeapBaseFlow[i]\
			.replace('\r','').replace('\n','').replace(' ',''))

	
	dssFile = HecDss.open(baseDir+'OUTPUT/DSS/'+DATE+'.dss')

	for ens_no in range(51):
		dataPath= "/OUTPUT/BAHADURABAD/FLOW//1DAY/EN-"+str(ens_no)+"/"
		print(dataPath)
		tsCont = dssFile.get(dataPath,1)
		times = tsCont.times
		values = tsCont.values
		
		bfAeddedValues = addBaseFlow(times,values,leapBaseFlow,nonLeapBaseFlow)

		# [replace data in same path]
		finalTsCont =  TimeSeriesContainer()
		finalTsCont.fullName = "/OUTPUT+BF/BAHADURABAD/FLOW//1DAY/EN-"+str(ens_no)+"/"
		finalTsCont.interval = tsCont.interval
		finalTsCont.values = bfAeddedValues
		finalTsCont.times = times
		finalTsCont.type = tsCont.type
		finalTsCont.units = tsCont.units
		finalTsCont.numberValues = tsCont.numberValues
		dssFile.put(finalTsCont)

	dssFile.done()

	return 0


def addBaseFlow(times,values,leapBaseFlow,nonLeapBaseFlow):
	
	for i in range(len(times)):

		timeOb = HecTime()
		timeOb.set(0)
		timeOb.addMinutes(times[i])
		year  = timeOb.year()
		
		if year%4==0:
			dayOfYear = timeOb.dayOfYear()
			baseFlow = leapBaseFlow[dayOfYear-1]
		else:
			dayOfYear = timeOb.dayOfYear()
			baseFlow = nonLeapBaseFlow[dayOfYear-1]

		values[i] = values[i] + baseFlow

	
	return values

if __name__ == '__main__':
	main()
