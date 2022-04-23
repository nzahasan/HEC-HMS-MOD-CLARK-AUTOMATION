#! /usr/bin/env python3
'''-------------------------------------------------------------
Produces two list of rating curve's with varying `a`

rating curve: c*(H-a)^b

H = water level
a = waterlevel at 0 discharge

devides the data in 2 section

wl < 80% quantile & wl >= 80% quantile

then creates equation for 2 dataset

can determine a by a= (h2^2 - h1*h3 )/(h1+h3-2*h2)

regression method followed is in kumar subramanya's book

Nazmul Ahasan
nzahasan@gmail.com
-------------------------------------------------------------'''


import pandas as pd

import numpy as np
import pylab as pl


def calc_nse(sim,obs):
    obsMean = obs.mean()
    sim_obs = (sim-obs)**2
    obs_obsMean = (obs-obsMean)**2

    return 1-(sim_obs.sum()/obs_obsMean.sum())





def regres(a,q,wl):

	x = np.log10(wl-a)
	y = np.log10(q)

	xy = x*y

	x2 = x**2
	y2 = y**2


	n=wl.shape[0]

	b = ( n*xy.sum() -x.sum()*y.sum()  ) / ( n*x2.sum() - (x.sum())**2 )

	c = 10**( ( y.sum() - b*x.sum() ) / n  )

	return [a,b,c]


def get_rating_eqn_data(a_start,a_end,q,wl):
	

	eqn_data=""
	for a in np.arange(a_start,a_end,-0.01):
		_,b,c = regres(a,q,wl)
		sim_q = c*(wl-a)**b
		nse = calc_nse(sim_q,q)
		eqn_data += "eqn: "+str("%.3f" % c)+"*(H-"+str(a)+")^"+str("%.3f" % b)+"\t nse: "+str("%.3f" % nse)+"\n"

	return eqn_data


def main():	
	
	obs_data = pd.read_csv("BH.OBS.2007-2017.WL+Q.csv")

	wl=obs_data["Water Level"]
	q=obs_data["Discharge"]


	# divide dset in 2 parts
	# set1_ : less than mean data
	# set2_ : greater than or equal to mean data

	mean_wl = wl.quantile(0.8)

	set1_wl=[]
	set1_q=[]

	set2_wl=[]
	set2_q=[]

	
	for i in range(wl.shape[0]):
		if wl[i] < mean_wl:
			set1_wl.append(wl[i])
			set1_q.append(q[i])
		if wl[i] >=mean_wl:
			set2_wl.append(wl[i])
			set2_q.append(q[i])

	set1_wl=np.asarray(set1_wl,dtype=np.float32)
	set1_q=np.asarray(set1_q,dtype=np.float32)

	set2_q=np.asarray(set2_q,dtype=np.float32)
	set2_wl=np.asarray(set2_wl,dtype=np.float32)


	with open("rating_curve_(wl<"+str(mean_wl)+").eqn","w") as file:
		file.write(get_rating_eqn_data( (wl.min()-0.01),0,set1_q,set1_wl) )

	with open("rating_curve_(wl>="+str(mean_wl)+").eqn","w") as file:
		file.write(get_rating_eqn_data( (wl.min()-0.01),0,set2_q,set2_wl) )

if __name__ == '__main__':
	main()