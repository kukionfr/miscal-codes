function main(){
	Dialog.create("Specify Stiffness");
	rows = 2;
	columns = 1;
	n = rows*columns;
	labels = newArray(n);
	defaults = newArray(n);
	labels[0] = "individual well,stiffness"; labels[1] = "Do All";
	defaults[0] = false; defaults[1] = true; 
	Dialog.addCheckboxGroup(rows,columns,labels,defaults);
	Dialog.show();
	single_on = Dialog.getCheckbox();
	all_on = Dialog.getCheckbox();

	//input = getDirectory("Input directory");
	input = "//serverdw/Pei-Hsun Wu 2/Stiffness and Chromosome instability project/Data/ASproject phase 4x scanning/WellView/"
	if (all_on){
	}
	if (single_on){
		Dialog.create("Type the cell-line + stiffness & choose top or bottom row");
		Dialog.addNumber("cell line", 304);
		Dialog.addString("stiffness", "25kpa");
		labels = newArray(2); defaults = newArray(2); labels[0] = "top"; labels[1] = "bottom"; defaults[0] = false; defaults[1] = false;
		Dialog.addCheckboxGroup(2,1,labels,defaults);
		Dialog.show();
		cell_line = Dialog.getNumber();
		stiffness = Dialog.getString();
		top_on = Dialog.getCheckbox();
		bottom_on = Dialog.getCheckbox();
		search_stiffness = ".*" + "7_" + stiffness +".*";	
		if (cell_line==6){
			if (top_on){well="well06";name="sc6_top_"+stiffness;}
			if (bottom_on){well="well05";name="sc6_bottom_"+stiffness;}
		}	
		if (cell_line==304){
			if (top_on){well="well03";name="sc304_top_"+stiffness;}
			if (bottom_on){well="well04";name="sc304_bottom_"+stiffness;}
		}	
		if (cell_line==308){
			if (top_on){well="well02";name="sc308_top_"+stiffness;}
			if (bottom_on){well="well01";name="sc308_bottom_"+stiffness;}
		}
		search_well = ".*" + well +".*";
		makemovie(search_stiffness,search_well,name,input);
	}
}

function makemovie(searchstring,searchstring1,name,input){
	imagelist= getFileList(input);
	for (i = 0; i < lengthOf(imagelist) ; i++) { 
		if (matches(imagelist[i],searchstring) && matches(imagelist[i],searchstring1)){
			open(input + imagelist[i]);
			run("Enhance Contrast", "saturated=0.35");
			run("Apply LUT");
		}
	}
	run("Images to Stack", "name=Stack title=[] use");
	getDateAndTime(year, month, dayOfWeek, dayOfMonth, hour, minute, second, msec);
	output = input + "/movie_created_on_" + dayOfMonth + "th/";
	File.makeDirectory(output);
	saveAs("tiff",output + name +".tif");
}

setBatchMode(true); //hide all windows while running
main();
print ("completed");
wait(500);	  //wait 500ms before closing windows
selectWindow("Log"); 
run("Close");