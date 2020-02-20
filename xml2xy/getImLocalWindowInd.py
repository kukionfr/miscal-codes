import numpy as np 
from time import sleep
def getImLocalWindowInd(XY,imsz,wndra,skipstep):
	x = XY[0].astype(np.int) 
	y = XY[1].astype(np.int)

	edgex = np.argwhere(np.logical_or(x<wndra+1,x>(imsz[0]-wndra-1)))
	edgey = np.argwhere(np.logical_or(y<wndra+1,y>(imsz[1]-wndra-1)))
	edge = np.append(edgex,edgey)
	x = np.delete(x,edge)
	y = np.delete(y,edge)

	ccx = np.logical_and((x<(imsz[0]-wndra+1)),(x>wndra))
	ccy = np.logical_and((y<(imsz[1]-wndra+1)),(y>wndra))
	cc = np.logical_and(ccx,ccy)
	
	xmin = x-wndra
	ymin = y-wndra

	indmin = np.ravel_multi_index((ymin-1,xmin-1),dims=imsz,mode='clip',order='F')

	meshx = np.arange(0,(2*wndra)+1,skipstep)*imsz[0]
	meshy = np.arange(0,(2*wndra)+1,skipstep)
	gx,gy=np.meshgrid(meshx,meshy)
	gxy=gx+gy
	gxy=gxy.T.flatten()
	
	if len(imsz)==3:
		for k in range(2)+1:
			gxy=np.hstack(gxy,gxy+k*imsz[0]*imsz[1])

	ind = np.tile(indmin,(len(gxy),1))+np.tile(np.asmatrix(gxy).T,(1,len(indmin)))
	notcc = np.invert(cc)
	inx = np.argwhere(notcc)
	if len(inx)!=0:inx =np.argwhere(notcc)[0][0]

	#ind[inx]=[0] #error x len is 2288, inx is 1648, ind is only 121.
	ind = np.round(ind)
	return ind.T