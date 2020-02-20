import numpy as np
import os
import time
from PIL import Image, ImageFilter, ImageDraw


#im is ndarray grey or pil
def smartcrop(imrgb,im,pil):
	if type(im) is not np.ndarray:
		#print 'input is PIL image'
		pix = np.asarray(im)
		im = np.asarray(im)
	if type(im) is np.ndarray:
		#print 'input is ndarray'
		pix = im
	pix.flags.writeable = True
	im.flags.writeable = True
	pix[pix<70]=0

	margin=0

	### horizontal crops
	sumlist = np.sum(pix,axis=1)
	#split image by zero separator gotta fix this...
	subarr = np.split(sumlist,np.where(sumlist==0)[0][0:1])
	#remove zero
	subarr = [np.delete(_,np.argwhere(_==0)) for _ in subarr]
	#pick largest region
	sizes = [len(_) for _ in subarr]
	large = [_ for _ in subarr if len(_)==max(sizes)][0]
	#crop this region
	croptarget_top = np.argwhere(sumlist==large[0])[-1][0]+margin #beginning of large region, last match
	croptarget_bot = np.argwhere(sumlist==large[-1])[0][0]-margin #end of large region, first match
	pix = pix[croptarget_top:croptarget_bot]
	im = im[croptarget_top:croptarget_bot]

	### vertical crop
	sumlistv = np.sum(pix,axis=0)
	#split image by zero separator
	subarrv = np.split(sumlistv,np.where(sumlistv==0)[0][0:1])
	#remove zero
	subarrv = [np.delete(_,np.argwhere(_==0)) for _ in subarrv]
	#pick largest region
	sizesv = [len(_) for _ in subarrv]
	largev = [_ for _ in subarrv if len(_)==max(sizesv)][0]
	#crop this region
	croptarget_R = np.argwhere(sumlistv==largev[0])[-1][0]+margin #beginning of large region, last match
	croptarget_L = np.argwhere(sumlistv==largev[-1])[0][0]-margin #end of large region, first match
	# pix = pix.T[croptarget_R:croptarget_L]
	# pix = pix.T
	im = im.T[croptarget_R:croptarget_L]
	im = im.T
	box = (croptarget_R,croptarget_top,croptarget_L,croptarget_bot)
	x_rad = (croptarget_L-croptarget_R)/2
	y_rad = (croptarget_bot-croptarget_top)/2
	rad = np.minimum(x_rad,y_rad)
	imrgb = imrgb.crop(box)
	if pil == 'pil':
		im = Image.fromarray(im)
		return imrgb,im,rad
	if pil == 'np':
		return imrgb,pix,rad

# cwd=os.path.abspath(os.path.dirname(__file__))
# imlist = [os.path.join(cwd,_) for _ in os.listdir(cwd) if _.endswith(".jpg")]
# k = 1
# a = Image.open(imlist[k])
# print imlist[k]
# ag = a.convert(mode="L")
# im = ag
# im_cropped = smartcrop(im,'np')
# im_cropped = Image.fromarray(im_cropped)
# im_cropped.show()
