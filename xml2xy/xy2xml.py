import numpy as np
import os
from lxml import etree as ET


def xy2xml(x,y,imagename):
	root = ET.Element("CellCounter_Marker_File")
	child = ET.SubElement(root, "Image_Properties")
	grandchild = ET.SubElement(child, "Image_Filename")
	grandchild.text = imagename
	child1 = ET.SubElement(root, "Marker_Data")
	grandchild1 = ET.SubElement(child1, "Current_Type")
	grandchild1.text = str(0)
	grandchild2 = ET.SubElement(child1, "Marker_Type")
	grandgrandchild = ET.SubElement(grandchild2, "Type")
	grandgrandchild.text = str(1)
	XY=np.vstack((x,y))
	for count,elem in enumerate(XY.T):
		grandgrandchild1 = ET.SubElement(grandchild2, "Marker")
		markerX = ET.SubElement(grandgrandchild1, "MarkerX")
		markerY = ET.SubElement(grandgrandchild1, "MarkerY")
		markerZ = ET.SubElement(grandgrandchild1, "MarkerZ")
		markerX.text = str(elem[0])
		markerY.text = str(elem[1])
		markerZ.text = str(1)

	for i in range(7):
		grandchild2 = ET.SubElement(child1, "Marker_Type")
		grandgrandchild = ET.SubElement(grandchild2, "Type")
		grandgrandchild.text = str(i+2)

	et = ET.ElementTree(root)
	dst= os.path.splitext(imagename)[0]+'.xml'
	et.write(dst, xml_declaration=True, encoding='UTF-8', pretty_print=True)
