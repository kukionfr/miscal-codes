import math
import numpy as np
import os
from PIL import Image, ImageDraw
from getImLocalWindowInd import getImLocalWindowInd
from imagej_xml_to_xy import xml2xy
from time import sleep, time


#import scipy.io

def true_sample_generator():
	start = time()

	cwd = os.path.abspath(os.path.dirname(__file__))
	imagebox = os.path.join(cwd,'well image stitch')
	mapbox = os.path.join(imagebox,'counting map')

	xmlist = [os.path.join(mapbox,_) for _ in os.listdir(mapbox) if ('xml' and 'CellCounter') in _]
	xmlist = [_ for _ in xmlist if not 'V2' in _]
	xmlist = [_ for _ in xmlist if not 'bad' in _]
	searchword = [os.path.basename(xmlist[_]).replace('.xml','').replace('CellCounter_','') for _,elem in enumerate(xmlist)]
	imlist = []
	for i in range(len(searchword)):
		im = [os.path.join(imagebox,_) for _ in os.listdir(imagebox) if searchword[i] in _]
		imlist.append(im[0])

	# xmlist_view = np.array(xmlist)[np.newaxis].T
	# imlist_view = np.array(imlist)[np.newaxis].T
	wndra = 30
	true_sample = np.empty(shape=(0,wndra+1,wndra+1))
	for i in range(len(xmlist)):
		activexml = xmlist[i]
		activeimg = imlist[i]
		XY = xml2xy(activexml)
		#scipy.io.savemat('test.mat',dict(x=XY[0].astype('int'),y=XY[1].astype('int')))
		im = Image.open(activeimg)
		imsz = im.size[::-1]
		skipstep = 2
		ind = getImLocalWindowInd(XY,imsz,wndra,skipstep)
		im = np.asarray(im)
		im = im.flatten('F')
		indarr = np.asarray(ind)
		imstack = np.empty(shape=(len(indarr),wndra+1,wndra+1))
		for count,elem in enumerate(imstack):
			imstack[count] = im[indarr[count]].reshape(wndra+1,wndra+1)
		true_sample = np.vstack((true_sample,imstack))
	imlabel = ['cell']*len(true_sample)
	end = time()
	print ('cutting took -- {:4.2f}sec'.format(end-start))
	return true_sample,imlabel

def slow_loop(falseXY,im,XY,sectionsize,distance):
	for x1 in np.arange(1,im.size[0],sectionsize,dtype='int'):
		if ((x1-1)%500)==0:print(x1)
		for y1 in np.arange(1,im.size[1],sectionsize,dtype='int'):
			flag = 0
			for count,elem in enumerate(XY.T):
				x2 = elem[0]
				y2 = elem[1]
				dist = np.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
				if dist > distance: flag = flag + 1
			if flag == len(XY.T):
				falseXY = np.vstack((falseXY,np.array([x1,y1])))
	return falseXY


def false_sample_generator():
	start = time()

	cwd = os.path.abspath(os.path.dirname(__file__))
	imagebox = os.path.join(cwd,'well image stitch')
	mapbox = os.path.join(imagebox,'counting map')

	xmlist = [os.path.join(mapbox,_) for _ in os.listdir(mapbox) if ('xml' and 'CellCounter') in _]
	xmlist = [_ for _ in xmlist if not 'V2' in _]
	xmlist = [_ for _ in xmlist if not 'bad' in _]
	searchword = [os.path.basename(xmlist[_]).replace('.xml','').replace('CellCounter_','') for _,elem in enumerate(xmlist)]
	imlist = []
	for i in range(len(searchword)):
		im = [os.path.join(imagebox,_) for _ in os.listdir(imagebox) if searchword[i] in _]
		imlist.append(im[0])

	# xmlist_view = np.array(xmlist)[np.newaxis].T
	# imlist_view = np.array(imlist)[np.newaxis].T
	wndra = 30
	false_rel_len = 1
	false_sample = np.empty(shape=(1,wndra+1,wndra+1))
	for i in range(len(xmlist)):
		activexml = xmlist[i]
		activeimg = imlist[i]
		print(activeimg)
		XY = xml2xy(activexml).astype('int')
		falseXY = np.empty(shape=(0,2))
		im = Image.open(activeimg)
		sectionsize= 100
		distance = wndra*1.414*4
		a = time()
		falseXY = slow_loop(falseXY,im,XY,sectionsize,distance)
		b = time()
		print('one loop: '+str(b-a))
		if len(falseXY)<int(len(XY.T)*false_rel_len):
			print('false coordinates are too small -> check distance calc part')
			falseXY = np.empty(shape=(0,2))
			sectionsize= 50
			distance = distance/2
			a = time()
			falseXY = slow_loop(falseXY,im,XY,sectionsize,distance)
			b = time()
			print('one loop: '+str(b-a))
		if len(falseXY)<int(len(XY.T)*false_rel_len):
			print('false coordinates are too small -> check distance calc part')
			falseXY = np.empty(shape=(0,2))
			sectionsize= 10
			distance = distance/2
			a = time()
			falseXY = slow_loop(falseXY,im,XY,sectionsize,distance)
			b = time()
			print('one loop: '+ str(b-a))
		if len(falseXY)<int(len(XY.T)*false_rel_len):
			print('false coordinates are too small -> check distance calc part')
			falseXY = np.empty(shape=(0,2))
			sectionsize= 2
			distance = distance/2
			a = time()
			falseXY = slow_loop(falseXY,im,XY,sectionsize,distance)
			b = time()
			print('one loop: '+ str(b-a))	
		falseXY = falseXY[np.random.choice(falseXY.shape[0], int(len(XY.T)*false_rel_len), replace=False), :]
		falseXY = falseXY.T.astype('int')
		
		#scipy.io.savemat('test.mat',dict(x=XY[0].astype('int'),y=XY[1].astype('int')))
		imsz = im.size[::-1]
		skipstep = 2
		ind = getImLocalWindowInd(falseXY,imsz,wndra,skipstep)
		im = np.asarray(im)
		im = im.flatten('F')
		indarr = np.asarray(ind)
		imstack = np.empty(shape=(len(indarr),wndra+1,wndra+1))
		for count,elem in enumerate(imstack):
			imstack[count] = im[indarr[count]].reshape(wndra+1,wndra+1)
		false_sample = np.vstack((false_sample,imstack))
	imlabel = ['notcell']*len(false_sample)
	end = time()
	print ('cutting took -- {:4.2f}sec'.format(end-start))
	return false_sample,imlabel

st = time()
true_sample,true_imlabel=true_sample_generator()
print('true sample --- '+str(time()-st))
false_sample,false_imlabel=false_sample_generator()
print('false sample --- '+str(time()-st))
np.save('true_sample_01.npy',true_sample)
np.save('true_imlabel_01.npy',true_imlabel)
np.save('false_sample_01.npy',false_sample)
np.save('false_imlabel_01.npy',false_imlabel)
print('save --- '+str(time()-st))

# im_draw = ImageDraw.Draw(im)
# for centroid in XY.T:
# 	x = centroid[0].astype(np.int)
# 	y = centroid[1].astype(np.int)
# 	rd = 20
# 	e=[x-rd,y-rd,x+rd,y+rd]
# 	im_draw.ellipse(e,fill='rgb(100%,100%,100%)')
# del im_draw
# im.show()

