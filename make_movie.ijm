function main(){
	Dialog.create("Specify Stiffness");
	rows = 9;
	columns = 1;
	n = rows*columns;
	labels = newArray(n);
	defaults = newArray(n);
	labels[0] = "plastic"; labels[1] = "25kpa_main"; labels[2] = "500pa"; labels[3] = "25kpa_old"; labels[4] = "25kpa_oldpassed"; labels[5] = "25kpa_original"; labels[6] = "500pa_on_plastic"; labels[7]="25kpa_on_plastic"; labels[8] = "Do All"; 
	defaults[0] = false; defaults[1] = false; defaults[2] = false; defaults[3] = false; defaults[4] = false; defaults[5] = false; defaults[6] = false; defaults[7] = false; defaults[8] = true; 
	Dialog.addCheckboxGroup(rows,columns,labels,defaults);
	Dialog.show();
	plastic_on = Dialog.getCheckbox();
	hard_on = Dialog.getCheckbox();
	soft_on = Dialog.getCheckbox();
	old_on = Dialog.getCheckbox();	
	oldpassed_on = Dialog.getCheckbox();
	hard_original = Dialog.getCheckbox();
	softtoplastic_on = Dialog.getCheckbox();
	hardtoplastic_on = Dialog.getCheckbox();
	all_on = Dialog.getCheckbox();

	//input = getDirectory("Input directory");
	input = "//serverdw/Pei-Hsun Wu 2/Stiffness and Chromosome instability project/Data/ASproject phase 4x scanning/PlateView/"
	if (all_on){
		searchstring = ".*plastic_kyu.*";searchstring1 = ".*Plastic_Evelyn.*";searchstring2 = ".*Plastic_evelyn.*";name = "plastic"; makemovie2(searchstring,searchstring1,searchstring2,name,input);
		searchstring = ".*main.*";name = "25kpa_main"; makemovie(searchstring,name,input);
		searchstring = ".*25kpa_old_kyu.*";searchstring1 = ".*25kpa_old_Evelyn.*";searchstring2 = ".*25kpa_old_evelyn.*";name ="25kpa_old"; makemovie2(searchstring,searchstring1,searchstring2,name,input);
		searchstring = ".*oldpassed.*";name = "25kpa_oldpassed"; makemovie(searchstring,name,input);
		searchstring = ".*500pa_kyu.*";searchstring1 = ".*500pa_Evelyn.*";searchstring2 = ".*500pa_evelyn.*";name ="500pa"; makemovie2(searchstring,searchstring1,searchstring2,name,input);
		searchstring = ".*25kpa_kyu.*";searchstring1 = ".*25kpa_evelyn.*";searchstring2 = ".*25kpa_Evelyn.*";name ="25kpa"; makemovie2(searchstring,searchstring1,searchstring2,name,input);
		searchstring = ".*500passed_kyu.*";searchstring1 = ".*500passed_Evelyn.*";searchstring2 = ".*500passed_evelyn.*";name ="500pa_passed"; makemovie2(searchstring,searchstring1,searchstring2,name,input);
		searchstring = ".*25passed_kyu.*";searchstring1 = ".*25passed_Evelyn.*";searchstring2 = ".*25passed_evelyn.*";name ="25kpa_on_plastic"; makemovie2(searchstring,searchstring1,searchstring2,name,input);
	}
	if (plastic_on){searchstring = ".*plastic_kyu.*";searchstring1 = ".*Plastic_Evelyn.*";searchstring2 = ".*Plastic_evelyn.*";name = "plastic"; makemovie2(searchstring,searchstring1,searchstring2,name,input);}
	if (hard_on){searchstring = ".*main.*";name = "25kpa_main"; makemovie(searchstring,name,input);}
	if (soft_on){searchstring = ".*500pa_kyu.*";searchstring1 = ".*500pa_Evelyn.*";searchstring2 = ".*500pa_evelyn.*";name ="500pa"; makemovie2(searchstring,searchstring1,searchstring2,name,input);}
	if (old_on){searchstring = ".*25kpa_old_kyu.*";searchstring1 = ".*25kpa_old_Evelyn.*";searchstring2 = ".*25kpa_old_evelyn.*";name ="25kpa_old"; makemovie2(searchstring,searchstring1,searchstring2,name,input);}
	if (oldpassed_on){searchstring = ".*oldpassed.*";name = "25kpa_oldpassed"; makemovie(searchstring,name,input);}
	if (hard_original){searchstring = ".*25kpa_kyu.*";searchstring1 = ".*25kpa_evelyn.*";searchstring2 = ".*25kpa_Evelyn.*";name ="25kpa"; makemovie2(searchstring,searchstring1,searchstring2,name,input);}
	if (softtoplastic_on){searchstring = ".*500passed_kyu.*";searchstring1 = ".*500passed_Evelyn.*";searchstring2 = ".*500passed_evelyn.*";name ="500pa_on_plastic"; makemovie2(searchstring,searchstring1,searchstring2,name,input);}
	if (hardtoplastic_on){searchstring = ".*25passed_kyu.*";searchstring1 = ".*25passed_Evelyn.*";searchstring2 = ".*25passed_evelyn.*";name ="25kpa_on_plastic"; makemovie2(searchstring,searchstring1,searchstring2,name,input);}
}

function makemovie(searchstring,name,input){
	imagelist= getFileList(input);
	for (i = 0; i < lengthOf(imagelist) ; i++) { 
		if (matches(imagelist[i],searchstring)){
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

function makemovie1(searchstring,searchstring1,name,input){
	imagelist= getFileList(input);
	for (i = 0; i < lengthOf(imagelist) ; i++) { 
		if (matches(imagelist[i],searchstring) || matches(imagelist[i],searchstring1)){
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
function makemovie2(searchstring,searchstring1,searchstring2,name,input){
	imagelist= getFileList(input);
	for (i = 0; i < lengthOf(imagelist) ; i++) { 
		if (matches(imagelist[i],searchstring) || matches(imagelist[i],searchstring1) || matches(imagelist[i],searchstring2)){
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