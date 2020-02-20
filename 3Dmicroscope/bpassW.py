import numpy as np
import time
from fspecial import *
from scipy import ndimage


def bpassW(arr,lnoise,lobject):
	b = float(lnoise)
	w = int(round(lobject))
	N=2*w+1
	hg=fspecial(N,b*np.sqrt(2)) #gaussian
	#ha=fspecial_avg(N) #avg
	ha = 0.0204 *np.ones(shape=(N,N))
	arr = np.asarray(arr)
	arra = ndimage.filters.convolve(input=arr,weights =hg-ha,mode='reflect') 
	arra[arra<0]=0
	rest=arra
	return rest

