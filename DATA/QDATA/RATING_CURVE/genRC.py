#! /usr/bin/env python3
'''------------------------------------------------------------
Produces a list of rating curve with varying a

rating curve: c*(H-a)^b

H = water level
a = waterlevel at 0 discharge

can determine a by a= (h2^2 - h1*h3 )/(h1+h3-2*h2)

regression method followed is in kumar subramanya's book

Nazmul Ahasan
nzahasan@gmail.com
------------------------------------------------------------'''

 
import pandas as pd
import numpy as np
import pylab as pl


def calc_nse(sim,obs):
    obsMean = obs.mean()
    sim_obs = (sim-obs)**2
    obs_obsMean = (obs-obsMean)**2
    return 1-(sim_obs.sum()/obs_obsMean.sum())


def regression(a,q,wl):

	# regression data
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
		_,b,c = regression(a,q,wl)
		sim_q = c*(wl-a)**b
		nse = calc_nse(sim_q,q)
		eqn_data += "eqn: "+str("%.3f" % c)+"*(H-"+str(a)+")^"+str("%.3f" % b)+"\t nse: "+str("%.3f" % nse)+"\n"

	return eqn_data


def main():	
	
	# read discharge and wl data
	obs_data = pd.read_csv("BH.OBS.2007-2017.WL+Q.csv")

	wl=obs_data["Water Level"]
	q=obs_data["Discharge"]


	with open("rating_curve.eqn","w") as file:
		file.write(get_rating_eqn_data( (wl.min()-0.01),0,q,wl) )

if __name__ == '__main__':
	main()