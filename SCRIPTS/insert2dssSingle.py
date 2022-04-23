"""-------------------------------------------------------------------------
This script inserts a single SHG grid rainfall into dss file

UTC:+06 version

Dependency:-
	-asc2dssGrid.exe/asc2dssGrid.sh (provided by hec)
Usage: insert2dss.py asc2dssGrid.sh-path dss-file-path input-raster-file
Nazmul Ahasan Shawn
-------------------------------------------------------------------------"""

import sys,os
from datetime import datetime,timedelta

if len(sys.argv)>=5:
	asc2dssPath = sys.argv[1]
	dssFile = sys.argv[2]
	SHGgridFile = sys.argv[3]
	insertDate = sys.argv[4]
else:
	print('insert2dss.py:Insufficient Argument\
		\n============================== \
		\nPlease Provide the followings:- \
		\n\t# asc2dssGrid.sh path \
		\n\t# Dss file path \
		\n\t# SHG grid file \
		\n\t# date' \
		)
	sys.exit()



if SHGgridFile.endswith('.asc'):

	date = datetime.strptime(insertDate,'%Y%m%d')

	milFmtDateStart = datetime.strftime(date,'%d%b%Y')
	milFmtDateEnd = datetime.strftime(date+timedelta(days=1),'%d%b%Y')
	
	# Bangladesh is in timezone +06:00 UTM, hence 06:00-06:00 
	savePath='/SHG10K/BRAHMAPUTRA/PRECIP/'+milFmtDateStart+':0600/'+milFmtDateEnd+':0600/CPC-EC/'

	dssCmd = asc2dssPath \
	+ ' INPUT=' + SHGgridFile  \
	+ ' DSSFILE=' + dssFile \
	+ ' PATHNAME='+ savePath \
	+ ' GRIDTYPE=SHG DTYPE=PER-CUM DUNITS=MM ZL=TRUE'

	output = os.popen(dssCmd).read()
	# assuming this means success :/
	if 'DSS---ZCLOSE Unit:' in output:
		print('>> Filled '+SHGgridFile.split('/')[-1]+' into DSS for date '+insertDate) 
	# print(output)
	# break