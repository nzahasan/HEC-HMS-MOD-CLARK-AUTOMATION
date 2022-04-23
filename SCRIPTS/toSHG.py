"""--------------------------------------------------------------------------------:
This script converts all raw raster grids in 
a directory to SHG GRID for hec-hms model input 

SHG-Grid projection :- 
	Asia South Albers Equal Area Conic

Extent of SHG grid:-
	X: -5100000 to -3200000
	Y: 4130000 to 4770000

Dependency:-
	- GDAL(2.2.1)

example: 
	toSHG.py input-raster-folder output-raster-folder projection-path
		[date format:YYYY-MM-DD]

Nazmul Ahasan Shawn
--------------------------------------------------------------------------------"""
import os, sys
from datetime import datetime,date,timedelta

def main():
	if len(sys.argv)>=4:
		RawRasterPath = sys.argv[1]

		if RawRasterPath[-1]!='/':
			RawRasterPath+='/'

		shgOutPath = sys.argv[2]

		if shgOutPath[-1]!='/':
			shgOutPath+='/'

		prjPath = sys.argv[3]

		if prjPath[-1]!='/':
			prjPath+='/'
		
	else:
		print('toSHG.py:Insufficient Argument\
		\n============================== \
		\nPlease Provide the followings:- \
		\n\t# Input Raster Directory \
		\n\t# SHG Grid output Directory\
		\n\t# Projection Directory' \
		)
		sys.exit()

	for rasterFile in os.listdir(RawRasterPath):
		if rasterFile.endswith('.asc'):
			
			print('Converting :'+rasterFile)
			inFile = RawRasterPath+rasterFile

			outFile = shgOutPath+rasterFile
			
			gdalCmd = 'gdalwarp \
				-s_srs '+prjPath+'/4326.prj \
				-t_srs '+prjPath+'/102028.prj \
				-te -5100000 4130000 \
				-3200000 4770000 \
				-tr 10000 10000 \
				-tap \
				-r bilinear \
				-dstnodata -99999 \
				'+inFile+' /vsistdout/ \
				| gdal_translate -of AAIGrid -co DECIMAL_PRECISION=3 /vsistdin/ \
				'+outFile

			# print(gdalCmd)
			os.system(gdalCmd)
			
			'''------------------------------------------------------:
			: remove leading spaces according to the suggestion
			: of Thomas Evans(Thomas.A.Evans@usace.army.mil)
			-------------------------------------------------------'''

			with open(outFile,'r') as outSHGfile:
				SHGlines = outSHGfile.readlines()
			
			leadingSpaceRemovedSHGtext=''
			
			for line in SHGlines:
				leadingSpaceRemovedSHGtext += line.lstrip()
			
			with open(outFile,'w') as outSHGfile:
				outSHGfile.write(leadingSpaceRemovedSHGtext)


if __name__ == '__main__':
	main()