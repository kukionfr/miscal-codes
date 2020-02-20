#!/usr/bin/env python
import numpy as np
import os
import time
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from bpassW import *
from decimal import Decimal
from math import pi
from matplotlib import pyplot as plt
from pkfndW2 import *
from scipy import ndimage
from skimage.draw import ellipse
from smartcrop import smartcrop
from xy2xml import *

from xml2xy import *


def format_e(n):
	a = '%E' % n
	return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]

def kukicounter(k):
	np.set_printoptions(precision=5,suppress=True)
	##load image
	#bb=pwd; ##current location of py file
	start = time.time()

	
	# k=5; 1 works well 2 as well
	
	#python index starts from 0, matlab index starts from 1
	print 'Counting the image --  '+ imlist[k]
	# a=double(imread([pth,imlist(k).name]));
	# a=uint16(a);
	# ag=rgb2gray(a);
	a = Image.open(imlist[k]) #flatten to greyscale 32bit floating
	ag = a.convert(mode="L")
	a,ag,radius = smartcrop(a,ag,'pil') 

	#ag.show() 
	# ag_np = np.asarray(ag)
	# print 'ag_np shape'
	# print ag_np.shape
	# ag = Image.fromarray(ag_np)
	# print 'ag shape'
	# print ag.size
	# #exclude the dark area
	# # ttc=max(ag,[],2)<10;
	# ttc = np.amax(ag,axis=1) < 10
	# # ttr=max(ag,[],1)<10;
	# ttr = np.amax(ag,axis=0) < 10
	# ag(ttc,:)=[]; 
	# ag[ttc]=[]
	# # ag(:,ttr)=[];
	# at.T[ttc]=[]
	# #reduce image size for fast processing
	# scf=0.5;
	scf=1
	# ag=imresize(ag,scf);
	resize = tuple(int(i*scf) for i in ag.size)
	ag = ag.resize(resize, Image.ANTIALIAS)
	a = a.resize(resize, Image.ANTIALIAS)
	# # display
	# s=sprintf('load/preprocess image finished -- %4.2fsec',toc);
	# disp(s)
	end = time.time()
	# print 'load/preprocess image finished -- {:10.4f} sec'.format(end-start)
	# #bg subtraction
	# bg1=mean(ag(:));
	ag = np.asarray(ag)
	
	pix = np.asarray(ag)
	pix.flags.writeable = True
	pix[pix<50]=0
	sumlist = np.sum(pix,axis=1)
	#split image by zero separator
	subarr = np.split(sumlist,np.where(sumlist==0)[0][0:1])
	#remove zero
	subarr = [np.delete(_,np.argwhere(_==0)) for _ in subarr]
	#pick largest region
	sizes = [len(_) for _ in subarr]
	large = [_ for _ in subarr if len(_)==max(sizes)][0]
	#crop this region
	croptarget = np.argwhere(sumlist==large[0])[-1][0]
	cropedgrey = pix[croptarget:]
	ag = cropedgrey


	a = np.asarray(a)
	a = a[croptarget:]
	a = Image.fromarray(a)

	bg1 = np.mean(ag)
	# imbr0=(single(ag)-single(bg1));
	imbr0 = ag-bg1
	# imbr=abs(imbr0);
	imbr = np.abs(imbr0)
	# s=sprintf('BackgroundSubstraciton finished -- %4.2fsec',toc); 
	# median = ag.filter(ImageFilter.MedianFilter)
	end = time.time()
	# print 'mean filter applied -- {:10.4f} sec'.format(end-start)   
	# disp(s);
	# #cell detection
	# b0=bpassW(double(imbr),1,3);
	b0 = bpassW(imbr,lnoise=1,lobject=3) #put median for median filter
	# ibg=mean(double(b0(:)))+1.5*std(double(b0(:)));

	# im = Image.fromarray(b0)
	# imbr=Image.fromarray(imbr)
	# im.show()
	# imbr.show()
	# time.sleep(5)
	var1=1.5
	ibg = np.mean(b0)+var1*np.std(b0)
	# pk=pkfndW2(b0,ibg,3);
	var2=3
	pk = pkfndW2(b0,ibg,var2)
	# pk5=pk;
	pk5=pk
	# cc=pk5(:,1)>0 & pk5(:,2)>0;
	cc=np.zeros(len(pk5))
	cc[pk5.T[0]>0]=True
	cc[pk5.T[1]>0]=True
	# pks=pk5(:,:);
	pks=pk5
	# s=sprintf('detected #%03.0f object inbound out of total %03.0f',sum(cc),length(cc));
	print 'detected {:3.0f} object inbound out of total {:3.0f}'.format(np.sum(cc),len(cc))
	# disp(s);
	# s=sprintf('Celldetection finished -- %4.2fsec',toc);  
	# print 'Celldetection finished -- {:4.2f} sec'.format(time.time()-start)  
	# disp(s);
	
	# disp(imlist(k).name);
	# #plotting
	# figure(1);
	# imagesc(b0);axis equal;
	# hold on;
	# plot(pks(:,1),pks(:,2),'g+');
	# hold off
	imsize = np.shape(ag)
	center = (imsize[0]/2,imsize[1]/2)
	radius = (radius-200)*scf 
	cent = pks.T
	x2 = cent[1]
	y2 = cent[0]
	distance = np.sqrt(np.square(center[0]-x2)+np.square(center[1]-y2))
	index_dist = np.argwhere(distance>(radius)).T[0]
	pks = np.delete(pks,index_dist,0)

	path01=os.path.split(imlist[k])[0]
	filename01 = os.path.split(imlist[k])[1]
	if os.path.exists(os.path.join(path01,'cropped_' + filename01)):
		targetxml = os.path.splitext(os.path.join(path01,'CellCounter_cropped_')+filename01)[0]+'.xml'
		XY_adjusted=xml2xy(targetxml)
		no_cells = len(XY_adjusted.T)*2
	else:
		# save xy to xml -> show imagej cell counter
		xy2xml(pks.T[1],pks.T[0],imlist[k])
		a.save(os.path.join(path01,'cropped_' + filename01),format="JPEG")
		no_cells = len(pks)*2 #multiply by 2 for diluted sample

	a_draw = ImageDraw.Draw(a)
	for centroid in pks:
		y = centroid[0]
		x = centroid[1]
		e=[x-1,y-1,x+1,y+1]
		a_draw.ellipse(e,fill='rgb(100%,0%,0%)')
	del a_draw
	# xsize = a.size[0]
	# ysize = a.size[1]
	#box = (100,100,xsize-100,ysize-100)
	#a=a.crop(box)
	#b=b.crop(box)
	#b.show()
	# figure(2);
	# imagesc(ag);axis equal; colormap gray
	# hold on;
	# plot(pk(:,1),pk(:,2),'r+',pks(:,1),pks(:,2),'g+');

	# hold off;
	# s=sprintf('Plotting finished -- %4.2fsec',toc);    
	print 'Plotting finished -- {:4.2f}sec'.format(time.time()-start)
	showstart = time.time()
	print 'showing image took -- {:4.2f}sec'.format(time.time()-start)
	area_px = pi*radius**2 
	px_size = 7.45 #um/px
	area_mm = area_px*(px_size*0.001)**2
	chamber_height = 0.1 #100nm
	chamber_vol = (area_mm*chamber_height)/1000
	density = format_e(Decimal(str(no_cells/chamber_vol)))
	densitye = Decimal(str(no_cells/chamber_vol))
	# print 'area in pixel -- {:4.2f}px^2'.format(area_px)
	# print 'pixel size-- {:4.2f}um/px'.format(px_size)
	# print 'area in mm -- {:4.2f}mm^2'.format(area_mm)
	# print 'chamber height-- {:4.2f}mm'.format(chamber_height)
	# print 'number of cells-- {:4.2f}'.format(no_cells)
	# print 'counted area volume-- {:4.8f}ml'.format(chamber_vol)
	print 'cell density-- {:.2E}cells/ml'.format(densitye) # 1.60E+6cells/ml
	#print 'cell density-- {:s}cells/ml'.format(density) #1.60344E+06cells/ml

	# get a font
	fnt = ImageFont.load_default()
	# get a drawing context
	d = ImageDraw.Draw(a)
	# draw text
	d.text((10,10), 'cell density-- {:.2E}cells/ml'.format(densitye), font=fnt, fill=(255,255,255))
	# draw text, full opacity
	#d.text((10,60), "World", font=fnt, fill=(255,255,255))
	file,ext=os.path.splitext(imlist[k])
	if not os.path.exists(file+'_counted.jpg'):
		a.save(file+'_counted.jpg',format="JPEG")




# cwd=os.path.abspath(os.path.dirname(__file__))
# cid=os.path.join(cwd,'08312018')
# # pth=[bb,'\'];
# # imlist=dir([pth,'\*.tif']);
# imlist = [os.path.join(cid,_) for _ in os.listdir(cid) if (_.endswith(".jpg") and not "counted" in _ and not "cropped" in _)]
# for k in range(len(imlist)):
# 	kukicounter(k)
kukicounter('C:/Users/kuki/Downloads/A3.jpeg')