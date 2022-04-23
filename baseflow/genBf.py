import numpy as np

def main():

	# [load Bf kernel]
	
	bf_kern = np.loadtxt('bh.bf.kern',delimiter="\t",skiprows=7)

	xin = bf_kern[:,0]
	yin = bf_kern[:,1]

	x365 = np.arange(1,366)
	x366 = np.arange(1,367)

	y365 = np.interp(x365,xin,yin)
	y366 = np.interp(x366,xin,yin)

	np.savetxt("bh.bf.365",y365,"%10.5f")
	np.savetxt("bh.bf.366",y366,"%10.5f")
	
	return

if __name__ == '__main__':
	main()