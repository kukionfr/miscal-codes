#!/usr/bin/env python

#built-in libraries
from time import sleep
from math import pi
from decimal import Decimal
import os

#basic libraries
import numpy as np 
from PIL import Image
#custom function
from xml2xy import *
# basic libraries
import numpy as np
import os
from PIL import Image
from decimal import Decimal
from math import pi
# built-in libraries
from time import sleep

# custom function
from xml2xy import *


def process(xls,im):
	XY=xml2xy(xls)
	no_cells= len(XY.T)
	img = Image.open(im)
	imsz = img.size
	radius = (np.min(imsz)/2)-200
	print radius
	area_px = pi*radius**2 
	px_size = 7.45 #um/px
	area_mm = area_px*(px_size*0.001)**2
	chamber_height = 0.1 #100nm
	chamber_vol = (area_mm*chamber_height)/1000
	densitye = Decimal(str(no_cells/chamber_vol))
	print im
	print 'cell density-- {:.2E}cells/ml'.format(densitye) 

cwd=os.path.abspath(os.path.dirname(__file__))
cid=os.path.join(cwd,'0829')
imlist = [os.path.join(cid,_) for _ in os.listdir(cid) if (_.endswith(".jpg") and 'cropped' in _)]
xlslist= [os.path.join(cid,_) for _ in os.listdir(cid) if (_.endswith(".xml") and 'cropped' in _)]
for count,elem in enumerate(xlslist):
	process(elem,imlist[count])