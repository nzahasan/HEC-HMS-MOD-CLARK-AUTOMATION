#! /usr/bin/env python3
"""-----------------------------------------------------------
This script converts ECMWF ENS Rainfall Data 
from netcdf to ArcInfo ASCII Raster file.
Projection: WGS1984

Dependency:-
	- NUMPY(1.13.1)
	- NETCDF4(1.2.9)
Usage: cpc2asc.py nc-file-name output-path

N.B: lat is in increasing order in nc files.

Nazmul Ahasan Shawn 
-----------------------------------------------------------"""

import sys,os
import numpy as np
from datetime import datetime
from datetime import timedelta
from netCDF4 import Dataset as ncopen


def main():
	#-------------------- get system argument --------------------#
	
	if len(sys.argv)>=4:

		try:
			ncfile = ncopen(sys.argv[1],'r')
		except:
			print("ERROR 200: Cant Read ECMWF NetCDF file.")
			return -200
		
		savePath = sys.argv[2]

		if savePath[-1] != '/':
			savePath+='/'

		REFTIME = datetime.strptime(sys.argv[3],'%Y%m%d')
	else:
		print('ecmwfNc2asc.py:Insufficient Argument\
		\n===================== \
		\nPlease Provide the followings:- \
		\n\t# NetCDF file path \
		\n\t# Output Path \
		\n\t# Date(YYYY-MM-DD)'\
		)
		sys.exit()

	
	nodata_value = -99999


	#-------------------- Extraction Boundary --------------------#
	lonStart = 70
	lonEnd = 100
	latStart = 20
	latEnd = 40
	
	#-------------------- Get all Prescious data --------------------#

	lats = ncfile.variables['g0_lat_2'][:]
	lons = ncfile.variables['g0_lon_3'][:]
	times = ncfile.variables['forecast_time4'][:]
	ensembles = ncfile.variables['ensemble0'][:]

	CP = ncfile.variables['CP_GDS0_SFC'][:]
	LSP = ncfile.variables['LSP_GDS0_SFC'][:]

	#------------------ select lat lon within bound ------------------#

	selectedLatID = []
	selectedLonID = []

	for latId in range(len(lats)):
		if lats[latId] >= latStart and lats[latId] <= latEnd:
			selectedLatID.append(latId)

	latsSelected = lats[ (selectedLatID[0]) : (selectedLatID[-1]+1) ]

	for lonId in range(len(lons)):
		if lons[lonId]>=lonStart and lons[lonId]<= lonEnd:
			selectedLonID.append(lonId)

	lonsSelected = lons[ (selectedLonID[0]) : (selectedLonID[-1]+1) ]



	# ---------------- ASC ----------------#

	# >> assuming cell size is same in both direction
	cellsize = abs(lonsSelected[0]-lonsSelected[1])
	nrows = len(latsSelected)
	ncols = len(lonsSelected)

	lowerXcorner = lonsSelected.min()-(cellsize/2)
	lowerYcorner = latsSelected.min()-(cellsize/2)

	header ="ncols\t\t\t"+ str(ncols) +"\n"\
			"nrows\t\t\t"+ str(nrows) +"\n"\
			"xllcorner\t\t"+ str(lowerXcorner) +"\n"\
			"yllcorner\t\t"+ str(lowerYcorner) +"\n"\
			"cellsize\t\t"+ str(cellsize) +"\n"\
			"NODATA_value\t"+ str(nodata_value)



	for ens_no in ensembles:
		
		for timeId in range(len(times)):
			if times[timeId]%24==0:
				
				# [extract daily rainfall from cumulative]
				if (timeId-4)<=0:
					prVal = CP[ens_no,timeId]+LSP[ens_no,timeId]
				else:
					prVal = (CP[ens_no,timeId]+LSP[ens_no,timeId]) - (CP[ens_no,timeId-4]+LSP[ens_no,timeId-4]) 

				prVal = prVal*1000	#>>m to mm conversion
				
				prVal = prVal.clip(min=0)

				if isinstance(prVal,np.ma.MaskedArray):
					prVal[prVal.mask] = nodata_value

				# >> saving file
				outPath = savePath+'EN-'+str(ens_no)+'/'
				if not os.path.exists(outPath):
					os.makedirs(outPath)
				
				filename = outPath+(REFTIME+timedelta(hours= int(times[timeId])-24 )).strftime('%Y%m%d')+'.en-'+str(ens_no)+'.asc'
				np.savetxt(filename, prVal ,delimiter=' ', newline='\n', header=header, comments='',fmt='%5.5f')
				print('RAW-ECMWF >> '+filename)

if __name__ == '__main__':
	main()
