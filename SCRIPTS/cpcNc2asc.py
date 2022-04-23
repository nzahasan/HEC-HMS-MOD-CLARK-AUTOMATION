#! /usr/bin/env python3
"""-----------------------------------------------------------
This script converts CPC Rainfall Data 
from netcdf to ArcInfo ASCII Raster file.
Projection: WGS1984

Dependency:-
	- NUMPY(1.13.1)
	- NETCDF4(1.2.9)
Usage: cpc2asc.py nc-file-name output-path

N.B: lat is in increasing order in nc files.

Nazmul Ahasan Shawn 
-----------------------------------------------------------"""

import sys
import numpy as np
from datetime import datetime
from datetime import timedelta
from netCDF4 import Dataset as ncopen


def main():
	#-------------------- get system argument --------------------#
	
	if len(sys.argv)>=3:
		try:
			ncfile = ncopen(sys.argv[1],'r')
		except:
			print("ERROR 20: Cant Read CPC NetCDF file.")
			return -20
		
		savePath = sys.argv[2]

		if savePath[-1] != '/':
			savePath+='/'
	else:
		print('cpc2asc.py:Insufficient Argument\
		\n===================== \
		\nPlease Provide the followings:- \
		\n\t# NetCDF file path \
		\n\t# Output Path' \
		)
		sys.exit()

	nodata_value = -99999

	#-------------------- Extraction Boundary --------------------#
	lonStart = 70
	lonEnd = 100
	latStart = 20
	latEnd = 40
	
	#-------------------- Get all Prescious data --------------------#

	REFTIME = datetime(1900, 1, 1, 00, 00,00) #will it change??
	lats = ncfile.variables['lat'][:]
	lons = ncfile.variables['lon'][:]
	times = ncfile.variables['time'][:] # time:units = "hours since 1900-01-01 00:00:00"
	prAll = ncfile.variables['precip'][:]

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

	cellsize = abs(lonsSelected[0]-lonsSelected[1]) # >> cell size is same in both direction
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

	# precipitation for writing
	for time_id in range(len(times)):
		
		# >> get pr for selected region
		prSelected = prAll[time_id,\
					(selectedLatID[0]):(selectedLatID[-1]+1),\
					(selectedLonID[0]):(selectedLonID[-1]+1)]
		
		prSelected._sharedmask = False
		if isinstance(prSelected,np.ma.MaskedArray):
			prSelected[prSelected.mask] = nodata_value
		
		# ------------------------------- save file ------------------------------------
		#: time here is accumulation start time(confirmed by Don Murray of ESRL ,thanks!)
		# ------------------------------------------------------------------------------
		
		filename = savePath+(REFTIME+timedelta(hours= int(times[time_id]) )).strftime('%Y%m%d')+'.asc'
		np.savetxt(filename, prSelected ,delimiter=' ', newline='\n', header=header, comments='',fmt='%5.5f')
		print('RAW-CPC >> '+filename)

if __name__ == '__main__':
	main()


