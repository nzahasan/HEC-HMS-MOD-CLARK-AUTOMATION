'''
	
	rating curve for bahadurabad
		- needs to be updated every year
	
	curve type: q = c*(wl-a)^n
	
	(2017)
	 < 18.47: 1.197*(H-4.35)^3.891
	>= 18.47: 0.016*(H-4.15)^5.505

Nazmul Ahasan
nzahasan@gmail.com
'''

import numpy as np
import sys

def qbyRC(wl):

	break_value = 18.47
	const = [	
		# for  < 18.47
		{ 'c':1.197, 'a':4.35, 'n':3.891 },
		# for >= 18.47
		{ 'c':0.016, 'a':4.15, 'n':5.505 }
	]
	
	# vectorize if its a numpy array
	if type(wl) is np.ndarray:

		if wl.ndim >1:
			print('Invalid data format: More than one dimension!')
			sys.exit()

		Q=  np.zeros(wl.shape[0])
		
		# create boolean mask
		mask_l  = wl<break_value
		mask_ge = wl>=break_value

		# (rc_eqn)
		Q[mask_l]  = const[0]['c']*( (wl[mask_l]-const[0]['a'])**const[0]['n'] )
		Q[mask_ge] = const[1]['c']*( (wl[mask_ge]-const[1]['a'])**const[1]['n'] )

		return Q
		
	else:
		
		Q = 0

		# (rc_eqn)
		if wl<break_value:
			Q = const[0]['c']*( (wl-const[0]['a'])**const[0]['n'] )
		elif wl>=break_value:
			Q =  const[0]['c']*( (wl-const[0]['a'])**const[0]['n'] )

		return Q

pass


