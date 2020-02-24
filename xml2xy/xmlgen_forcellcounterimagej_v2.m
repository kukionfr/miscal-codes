%input: xyzl n x 4 matrix  &  imagename in string
%output: xml file with xyz coordinates for imageJ cell counter

%input example:  xyz with label = [1,2,3,1;2,3,4,1;3,4,5,2;4,5,6,2;5,6,7,2;6,7,8,4;7,8,9,8] 
%               imagename = 'Capture.png'
% Kyu v1 07/16/2018
% last edit 10/14/2019
function xmlgen_forcellcounterimagej_v2(xyzlcoord,imagename)
    docNode = com.mathworks.xml.XMLUtils.createDocument('CellCounter_Marker_File');
    
    entry_node1 = docNode.createElement('Image_Properties');
    docNode.getDocumentElement.appendChild(entry_node1);
    
    filename_node = docNode.createElement('Image_Filename');
    entry_node1.appendChild(filename_node);
    
    filename_text = docNode.createTextNode(imagename);
    filename_node.appendChild(filename_text);
    
    entry_node2 = docNode.createElement('Marker_Data');
    docNode.getDocumentElement.appendChild(entry_node2);
    
    currenttype_node = docNode.createElement('Current_Type');
    entry_node2.appendChild(currenttype_node);
    
    currenttype_text = docNode.createTextNode('0');
    currenttype_node.appendChild(currenttype_text);
    
    markertype_node = docNode.createElement('Marker_Type');
    entry_node2.appendChild(markertype_node);
 for j = 1:length(unique(xyzlcoord(:,4)))
    disp(j)
    type_node = docNode.createElement('Type');
    markertype_node.appendChild(type_node);
    type_text_node = docNode.createTextNode(num2str(j));
    type_node.appendChild(type_text_node);
    % split matrix into lists by coordinate.
%     x = num2str(xyzlcoord(:,1));
%     y = num2str(xyzlcoord(:,2));
%     z = num2str(xyzlcoord(:,3));
    xyzlcoord=round(xyzlcoord);
    xyzlcoord_a=xyzlcoord(xyzlcoord(:,4)==j,:);
%     for i=1:length(xyzlcoord_a(:,1))
    for i = 1:8
        marker_node = docNode.createElement('Marker');
        markertype_node.appendChild(marker_node);
     
        markerx = docNode.createElement('MarkerX');
        marker_node.appendChild(markerx);
        
        markerx_text = docNode.createTextNode(num2str(xyzlcoord_a(i,1)));
        markerx.appendChild(markerx_text);
        
        markery = docNode.createElement('MarkerY');
        marker_node.appendChild(markery);
        
        markery_text = docNode.createTextNode(num2str(xyzlcoord_a(i,2)));
        markery.appendChild(markery_text);
        
        markerz = docNode.createElement('MarkerZ');
        marker_node.appendChild(markerz);
        
        markerz_text = docNode.createTextNode(num2str(xyzlcoord_a(i,3)));
        markerz.appendChild(markerz_text);
    end 
 end
    xmlwrite('coord.xml',docNode);
    type('coord.xml');
end