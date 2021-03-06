import numpy as np
import os
from PIL import Image
from matplotlib import pyplot as plt
from skimage import io, data, filters, color, measure, morphology, util
from skimage.viewer import ImageViewer

cwd = r'C:\Users\kuki\Desktop\nat prot\figure raw file\slide5\micropattern'
im_loc = os.path.join(cwd,'wild--_rgb.tif')
# imfiles = [_ for _ in os.listdir(cwd) if _.lower().endswith(('.tif','.tiff'))]
# imfilespath = [os.path.join(cwd,_) for _ in imfiles]
im = io.imread(im_loc)
img = color.rgb2gray(im)

val = filters.threshold_otsu(img)
adjust=0.035
mask = img<val-adjust
mask = util.invert(mask)
mask2=morphology.remove_small_objects(mask,min_size=64)

# io.imshow(mask2)
# io.show()

labels = measure.label(mask2,background=0)

# io.imshow(labels)
# io.show()

org_im= Image.open(im_loc)
green = (51,162,52)
brown = (136,82,76)
orange = (253,129,20)
pink = (231,149,207)
blue = (22,113,177)
skyblue = (22,189,207)
yellow = (198,198,71)
red = (223,57,59)
print(np.unique(labels))
for i in [1,3]:
	x= np.where(labels==i)[0]
	y= np.where(labels==i)[1]
	xy = zip(y,x)
	for loc in xy:
		org_im.putpixel(loc,green) 
for i in [4]:
	x= np.where(labels==i)[0]
	y= np.where(labels==i)[1]
	xy = zip(y,x)
	for loc in xy:
		org_im.putpixel(loc,red) 
for i in [2]:
	x= np.where(labels==i)[0]
	y= np.where(labels==i)[1]
	xy = zip(y,x)
	for loc in xy:
		org_im.putpixel(loc,brown) 		
org_im.show()
org_im.save(os.path.join(os.path.dirname(im_loc),'wild--_rgb_labeled.tif'))



