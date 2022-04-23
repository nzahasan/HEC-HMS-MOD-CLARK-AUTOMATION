#! /usr/bin/env python3

"""-------------------------------------------------

rating curve for bahadurabad (updated @ 2017 end)
	- needs to be updated every year

	curve type: q = c*(wl-a)^n


	2018:
		Q = 25.4 (h- 6.70)^2.92  for h<14.66
		Q = 540  (h-10.15)^1.992 for 14.66< h <17.86
		Q = 1000 (h-13.50)^2.20  for h>17.86

Nazmul Ahasan
nzahasan@gmail.com
-------------------------------------------------"""

import numpy as np
import sys

def qbyRC(wl):

	# just add nother block for extra segment
	params = [	
		{  'min':0,     'max':14.66, 'c':25.4,  'a':6.70,  'n':2.92  },		
		{  'min':14.66, 'max':17.86, 'c':540,   'a':10.15, 'n':1.992 },
		{  'min':17.86, 'max':22.00, 'c':1000,  'a':13.50, 'n':2.20  }
	]
	
	# vectorize if its a numpy array
	if type(wl) is np.ndarray:

		if wl.ndim >1:
			print('Invalid data format: More than one dimension!')
			sys.exit()

		Q =  np.ones(wl.shape[0])*-999
		

		for i in range(len(params)):

			# create boolean mask
			mask  = (wl >= params[i]['min']) & (wl < params[i]['max']) 

			Q[mask]  = params[i]['c']*( (wl[mask]-params[i]['a'])**params[i]['n'] )
		
		if Q[Q==-999].shape[0]>0:
			print('Warning: output has -999 values, break values didnt covered the full range')

		return Q
		
	else:
		
		Q = -999

		for i in range(len(params)):
			if wl >= params[i]['min'] and wl < params[i]['max']:
				Q = params[i]['c']*( (wl-params[i]['a'])**params[i]['n'] )
				break

		if Q==-999:
			print('Warning: output is -999, break values didnt covered the full range')
		
		return Q




