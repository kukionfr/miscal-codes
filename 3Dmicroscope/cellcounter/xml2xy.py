import numpy as np
import xml.etree.ElementTree as ET


def xml2xy(xmlfile):
	tree = ET.parse(xmlfile)
	root = tree.getroot()
	# if root.tag =='CellCounter_Marker_File': print 'correct file! ' + root.tag
	# else: print 'wrong file'

	coord = []
	for c in root:
		for ch in c:
			for chi in ch:
				for chil in chi:
					coord.append(chil.text)

	coord = [_ for _ in coord if _ != '1']

	X=[]
	Y=[]
	for index, elem in enumerate(coord):
		if index % 2 == 0: X.append(elem)
		else: Y.append(elem)
	XY = np.vstack((X,Y))
	return XY