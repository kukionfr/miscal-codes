import numpy as np
import os
import xml.etree.ElementTree as ET


def xml2xy(xmlfile):
	tree = ET.parse(xmlfile)
	root = tree.getroot()
	
	type1 = []
	type2 = []
	type3 = []
	type4 = []
	type5 = []
	type6 = []
	type7 = []
	type8 = []
	type9 = []

	chi_list=[]
	for c in root:
		for ch in c:
			for chi in ch:
				chi_list.append(chi)
	idxlist = []
	for idx,elem in enumerate(chi_list):
		if elem.tag=='Type': idxlist.append(idx)

	for chil in chi_list:
		
		for child in chil:
			type1.append(child.text)


				# splited = np.split(chi,np.argwhere(chi.tag=='Type'))

	# 			for chil in splited:
	# 				coord.append(chil.text)
	# coord = [_ for _ in coord if _ != '1']

	# X=[]
	# Y=[]
	# for index, elem in enumerate(coord):
	# 	if index % 2 == 0: X.append(elem)
	# 	else: Y.append(elem)
	# XY = np.vstack((X,Y))
	# return XY

xy = xml2xy('C:/Users/kuki/Desktop/CellCounter_xy01c1.xml')

# folder = 'C:/Users/kuki/Desktop/'
# xmllist = [_ for _ in os.listdir(folder) if _.endswith('xml')]
# for xmlfile in xmllist:
# 	xy = xml2xy(xmlfile)

