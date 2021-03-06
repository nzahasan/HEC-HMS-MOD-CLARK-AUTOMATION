'''
---------------------------------------------
This script extracts model result as csv

Nazmul Ahasan Shawn
nzahasan@gmail.com
---------------------------------------------
'''

from hec.script import *
from hec.heclib.dss import *
from hec.heclib.util import *
from hec.io import *


def main():
	# ___ arguments ___ #
	
	# [YYYYMMDD]
	date = "20180718"

	# [/home/nazmul/Workdir/MOD-CLARK/OUTPUT/DSS/2017-12-11.dss]
	dssFilePath = "/home/nazmul/ModelWOrk/MOD-CLARK/OUTPUT/DSS/20180718.dss"
	
	# [/home/nazmul/Workdir/MOD-CLARK/OUTPUT/CSV/2017-12-11/]
	outCsvDir= "/home/nazmul/ModelWOrk/MOD-CLARK/OUTPUT/CSV/20180718"
	
	if outCsvDir[-1]!='/':
		outCsvDir+='/'
	
	# _if changes fix it_
	dataPathPrefix = "/OUTPUT+BF/BAHADURABAD/FLOW//1DAY/"

	dssFile = HecDss.open(dssFilePath)

	for ens_no in range(51):
		dataPathName = dataPathPrefix+"EN-"+str(ens_no)+"/"
		print(dataPathName)		
	

		tsCont = dssFile.get(dataPathName,1)

		times = tsCont.times

		values = tsCont.values

		try:
			valLen = len(values)
		except:
			print('Error 10: No records found.')
			return -999

	
		csvStr = makeCSV(times,values)

		outCsvPath = outCsvDir+date+".en-"+str(ens_no)+".csv"
		# print(outCsvPath)
		# return
		open(outCsvPath,'w').write(csvStr)

	dssFile.done()

	return 0

def makeCSV(times,values):
	csvDat = ''

	for i in range(len(times)):
		timeOb = HecTime()
		timeOb.set(0)
		timeOb.addMinutes(times[i])


		csvDat += timeOb.date(4).replace(" ","")+' '+timeOb.time()+','+str(values[i])+'\n'
	return csvDat

if __name__ == '__main__':
	main()
