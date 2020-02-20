#!/usr/bin/env python
import datetime
import datetime
import numpy as np
import os
from PIL import Image, ImageFilter, ImageDraw, ImageFont
# import time
from bpassW import *
# from matplotlib import pyplot as plt
# from math import pi
from decimal import Decimal
from pkfndW2 import *
from skimage.draw import ellipse


# camera libraries
#from gpiozero import LED 
#from picamera import PiCamera 
#import io 

def format_e(n):
	a = '%E' % n
	return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]

def kukicounter(imagefile):
	np.set_printoptions(precision=5,suppress=True)
	# ## take photo
	# led = LED(17)
	# led.on()
	# print ("LED on")
	# body = camera.get_frame()
	# now = datetime.datetime.now()
	# dstfilename = "Kyu" + now.strftime("%Y-%m-%d %Hh%Mm")
	# with open(dstfilename,'wb') as f:
	# 	f.write(body)
	# 	f.close()
	# print("LED off")
	# led.off()
	#imagefile = 'C:/Users/kuki/Downloads/071910am/1b01.jpeg'
	## pre-processing
	a = Image.open(imagefile) # open image
	ag = a.convert(mode="L") # mode=L (8bit, black and white) aka greyscale
	scf=0.5
	resize = tuple(int(i*scf) for i in ag.size)
	ag = ag.resize(resize, Image.ANTIALIAS)
	a = a.resize(resize, Image.ANTIALIAS)
	ag = np.asarray(ag)

	bg1 = np.mean(ag)
	# mean filter: subtract mean of all pixels from each pixel 
	# noise-reduction
	imbr0 = ag-bg1 
	imbr = np.abs(imbr0)
	#ag=Image.fromarray(ag)
	#median = ag.filter(ImageFilter.MedianFilter)
	#ag=np.asarray(ag)
	## cell dectection 
	b0 = bpassW(imbr,lnoise=1,lobject=3) #put median for median filter
	
	var1=13
	ibg = np.mean(b0)+var1*np.std(b0)

	var2=20
	pk = pkfndW2(b0,ibg,var2)

	pk5=pk

	cc=np.zeros(len(pk5))
	cc[pk5.T[0]>0]=True
	cc[pk5.T[1]>0]=True
	pks=pk5

	no_cells = len(pks)*2

	print ('detected {:3.0f} object inbound out of total {:3.0f}'.format(np.sum(cc),len(cc)))
	

	# draw dot on top of cells
	a_draw = ImageDraw.Draw(a)
	for centroid in pks:
		y = centroid[0]
		x = centroid[1]
		e=[x-1,y-1,x+1,y+1]
		a_draw.ellipse(e,fill='rgb(100%,0%,0%)')
	del a_draw

	# area_px = 'imagesize' 
	# px_size = 7.45 #um/px
	# area_mm = area_px*(px_size*0.001)**2
	# chamber_height = 0.1 #100nm
	# chamber_vol = (area_mm*chamber_height)/1000
	# density = format_e(Decimal(str(no_cells/chamber_vol)))
	# densitye = Decimal(str(no_cells/chamber_vol))
	# print ('cell density-- {:.2E}cells/ml'.format(densitye)) 

	# get a font
	#fnt = ImageFont.load_default()
	# get a drawing context
	#d = ImageDraw.Draw(a)
	# draw text
	#d.text((10,10), 'cell density-- {:.2E}cells/ml'.format(densitye), font=fnt, fill=(255,255,255))
	# draw text, full opacity
	#d.text((10,60), "World", font=fnt, fill=(255,255,255))
	file,ext=os.path.splitext(os.path.basename(imagefile))

	# create destination folder
	desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
	dstfolder = os.path.join('C:/Users/kuki/Downloads/071910am','count_results')
	if not os.path.exists(dstfolder): os.mkdir(dstfolder)
	# prevent overwriting counted image
	if not os.path.exists(file+'_counted.jpg'):
		a.save(os.path.join(dstfolder,file+'_counted.jpg'),format="JPEG")
	return no_cells

	
fol='C:/Users/kuki/Downloads/071910am'
ims = [os.path.join(fol,_) for _ in os.listdir(fol) if _.endswith('jpeg')]
for im in ims:
	no_cells = kukicounter(im)
print(no_cells)