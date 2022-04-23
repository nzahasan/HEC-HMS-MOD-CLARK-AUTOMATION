#! /usr/bin/env python3
"""-------------------------------------------------------------------------
This script inserts SHG grid rainfall into dss file

UTC:+06 version

Dependency:-
	-asc2dssGrid.exe/asc2dssGrid.sh (provided by hec)
Usage: insert2dss.py asc2dssGrid.sh-path dss-file-path input-raster-directory
Nazmul Ahasan Shawn
-------------------------------------------------------------------------"""

import sys,os
from datetime import datetime,timedelta

def main():

	if len(sys.argv)>=4:
		asc2dssPath = sys.argv[1]
		dssFile = sys.argv[2]
		inSHGdir = sys.argv[3]
		
		if inSHGdir[-1]!='/':
			inSHGdir+='/'
		
	else:
		print('insert2dss.py:Insufficient Argument\
			\n============================== \
			\nPlease Provide the followings:- \
			\n\t# asc2dssGrid.sh path \
			\n\t# Dss file path \
			\n\t# Input SHG grid directory path' \
			)
		sys.exit()


	for SHGgridFile in os.listdir(inSHGdir):
		if SHGgridFile.endswith('.asc'):

			inputSHG = inSHGdir+SHGgridFile

			date = datetime.strptime(SHGgridFile.split('.')[0],'%Y%m%d')

			milFmtDateStart = datetime.strftime(date,'%d%b%Y')
			milFmtDateEnd = datetime.strftime(date+timedelta(days=1),'%d%b%Y')
			
			# Bangladesh timezone +06:00 UTM hence 06:00-06:00 
			savePath='/SHG10K/BRAHMAPUTRA/PRECIP/'+milFmtDateStart+':0600/'+milFmtDateEnd+':0600/CPC-EC/'

			dssCmd = asc2dssPath \
			+ ' INPUT=' + inputSHG  \
			+ ' DSSFILE=' + dssFile \
			+ ' PATHNAME='+ savePath \
			+ ' GRIDTYPE=SHG DTYPE=PER-CUM DUNITS=MM ZL=TRUE'

			output = os.popen(dssCmd).read()
			# assuming this means success :/
			if 'DSS---ZCLOSE Unit:' in output:
				print('>> Entered '+SHGgridFile+' into DSS') 
				
			pass

if __name__ == '__main__':
	main()