# Mod-Clark Model for Brahmaputra Basin  
`Version -3.7`  
`Testing OS - Ubuntu 16.04`  
`HEC-HMS:4.2.1`  
`Nazmul Ahasan Shawn`     

### Future work: 
	- add a data intigraty checker script
	- add bias correction (not that important)

### Notes: 
	- Upper case directory's are subject to change.  
		and lower case directory's contains static resources
	- To run HEC-HMS in headless mode add '-Djava.awt.headless=true'
	- Copy asc2dssGrid.sh in hec-hms-xxx directory. (important)
	- Wierd behavior if no tailing `/` provided in porject path   
		in `OpenProject()` function within runModel.py
	- Replacing project path with variable doesnt work!
	- No base-flow in upstream basin's of Bahadurabad , `addBaseFlow.py` adds it saperately after  
		each model run 
	- additional parsing of <:_xxx-xxx_:> tag is implemented  
		 because hec-hms dosent support sys arguments 
	- tar.gz files contains file permission detail, better use that instead of zip
	- Genereted forecast plot is of 17 day = -1 day + today + 15 day forecast

----

### Some Thanks  
	A huge thanks to HEC team for support. Specially:- 
	- Tom Evans, for providing asc2DssGrid.sh script(linux version of asc2DssGrid.exe) 
		& fix of compression bug (grid value > 327 leads to nodata cell) by adding ZL=TRUE
	- Tom Brauer, fix of failing to copy forecast output to a new dss file.

----

### Change-Log:
	
	1.2:
		- Added parseable tag for model path in run-date.sh
		- Added BaseFlow adding script
		- Fixed CPC data Time Issue
	
	1.5:
		- Baseflow time-series is corrected
		- Added a initial sleep in runModel.py script
		- Baseflow kernel updated
	
	2.0:
		- Added a recursive filter based baseflow seperation script (same method used is SWAT)
	
	2.1:
		- Fixed hindcast generation error by deleting forecast dss
		- Shell script updated
		- permission fix for scripts
	
	2.3:
		- Added `ZL=TRUE` flag for fixing bug: >327 value creates NO-DATA cell.
		- Added model output as csv and forecast plotter script
	
	2.5:
		- Added rating curve generation script
		- Model Recalibrated with 5 subbasin for performance improvement
	
	3.0:
		- Fixed multiple date format. all the data and output is in YYYYMMDD format
		- Added LSTM error correction model
		- Headless hec-hms script added.
		- Added WL downloader script form ffwc website
	
	3.1:
		- Added dependency installer script

	3.2:
		- Removed NAN for missing value in errCorr.py, and filled with previous day value
		- Removed fontnames from forecast plotter for X-platform compitibility

	3.3:
		- Added exceedence probability plot
		- Added cutline for forecast start date in plumes plot
		- Added requirements.txt file for easier python dependency installation
	
	3.5:
		- Discarded LSTM error correction model due to low amount of data and unreliablity
		- Added ARIMA ts forecasting model with failsafe to blending.
		- Updated probability plot
		- Added interpolation method for missing value in error feed
		- Included simulated date's > 20170701,20170806,20170904
		- Some permission fix
		- Fixed argument warning in errCorr.py and ffwcWL.py
	
	3.6:
		- Updated regx for ffwc bh data download
		- Fixed rating curve script error
		- ARIMA now returns nan if order is (0,0,0) so that blending can apply
		- Removed invalid cell from 'BRAHMA_MOD_CLARK.mod' file
	
	3.7:
		- Updated rating curve script for easier adding of another segment/block
		- Fixed waterlevel downloading script

#### Note: No further feature will be added after version 3.5. only bugfix will be applied if necessary.

