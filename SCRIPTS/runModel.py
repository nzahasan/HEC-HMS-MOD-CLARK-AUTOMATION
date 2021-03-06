'''-----------------------------------------------------------
Run Model for ECMWF 51 set ensemble precipitation forecast

Nazmul Ahasan Shawn
nzahasan@gmail.com
-----------------------------------------------------------'''

from hec.script import *
from hec.heclib.dss import *
from hec.heclib.util import *
from hec.io import *
from hms.model.JythonHms import *
import java,time

def main():
	# NEED TO REPLACE <:_***_:> TAGS ONLY

	DATE = '20180718'
	baseDir= '/home/nazmul/ModelWOrk/MOD-CLARK' 
	
	if baseDir[-1]!='/':
		baseDir+='/'

	BASE_CPC_DIR = baseDir+"DATA/DSS/CPC-RAINFALL/CPC-RAINFALL.dss"
	CPC_EC_DSS_DIR = baseDir+'DATA/DSS/CPC-ECMWF/'+DATE+'/'
	
	# get tagged grid control file data
	taggedGridCtlFilePath=baseDir+'res/BRAHMA_MOD_CLARK.grid.#'
	taggedGridCtlFile = open(taggedGridCtlFilePath,'r')
	taggedGridCtlData = taggedGridCtlFile.read()
	taggedGridCtlFile.close()

	# replace base cpc data dir
	taggedGridCtlData = taggedGridCtlData.replace("<:_base-cpc-dss_:>",BASE_CPC_DIR)

	for ens_no in range(51):
		# [write grit control file for this ensemble]

		dssFile = CPC_EC_DSS_DIR+DATE+'.en-'+str(ens_no)+'.dss'
		
		dssFile = baseDir+'DATA/DSS/CPC-ECMWF/'+DATE+'/'+DATE+'-CPC-EC-EN-'+str(ens_no)+'.dss'

		gridCtl = taggedGridCtlData.replace('<:_forecast-rf-dss_:>',dssFile)
		
		# closing the file important
		gridCtlFile = open(baseDir+'brahmaputra_model/BRAHMA_MOD_CLARK.grid','w')
		gridCtlFile.write(gridCtl)
		gridCtlFile.close()

		# [run model]
		print('\n ====== ENSEMBLE-'+str(ens_no)+' RUN  ====== \n')
		OpenProject("BRAHMA_MOD_CLARK", "/home/nazmul/ModelWOrk/MOD-CLARK/brahmaputra_model/")
		Compute("FORECAST")

		print("Copying Forecast Data...")
		
		failCount=0
		
		# __initial_sleep_dont_wake_it!__
		time.sleep(2)
		
		while True:

			if failCount>=10:
				print('ERROR:- Failed 10 or more attempt to copy result...')
				Exit(10)

			try:
				cpyData(baseDir,DATE,ens_no)
				print('Copied successfully.')
				break
			except:
				print('Failed copying. Waiting 2s...')
				failCount+=1
				time.sleep(2)

	Exit(1)

def cpyData(baseDir,DATE,ens_no):
		
		dssf = HecDss.open(baseDir+"brahmaputra_model/FORECAST.dss")

		data = dssf.get('//BAHADURABAD/FLOW//1DAY/RUN:FORECAST/',1)
		

		new_tsc = TimeSeriesContainer()

		new_tsc.fullName = "/OUTPUT/BAHADURABAD/FLOW//1DAY/EN-"+str(ens_no)+"/"
		new_tsc.interval = data.interval
		new_tsc.values = data.values
		new_tsc.times = data.times
		new_tsc.type = data.type
		new_tsc.units = data.units
		new_tsc.numberValues = data.numberValues

		out_dss = HecDss.open(baseDir+'OUTPUT/DSS/'+DATE+'.dss')
		out_dss.put(new_tsc)
		dssf.done()
		out_dss.done()

if __name__ == '__main__':
	main()
