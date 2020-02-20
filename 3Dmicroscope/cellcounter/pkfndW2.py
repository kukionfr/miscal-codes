import numpy as np
import time
from PIL import Image
from scipy import ndimage
from skimage.measure import regionprops
from skimage.morphology import disk, dilation


def intersect2d(A,B):
	aset = set([tuple(x) for x in A])
	bset = set([tuple(x) for x in B])
	return np.array([x for x in aset & bset])

def pkfndW2(im,th,sz):
	sz = np.round((sz-1)/2)
	if sz<0:sz=0
	h=disk(sz)
	imd = dilation(im,h)

	A = np.argwhere(im>th)
	B = np.argwhere(im==imd)
	C = intersect2d(A,B)
	st = C

	return st