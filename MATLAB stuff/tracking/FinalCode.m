% Name : Kyu Sang Han 
% Last Edited : July 15th 2016
% Last Location : UniOne 
% Path : C:\Users\Wirtz Lab Station\OneDrive\Kyu Tracking\General Tracking
close all; clear; clc; workspace; format compact; format shortG
%% locate folder with excel and tif files
start_path = fullfile('C:\Users\Wirtz Lab Station\Desktop\Kyu Tracking\General Tracking');
% user locate the folder starting from the start_path
folder_name = uigetdir(start_path);
% search all excel files
excelfiles = dir(strcat(folder_name,'\*.xlsx'));
tifFiles = dir(strcat(folder_name,'\*.tif'));
%% read excel file 
numtraj = length(excelfiles);
%preallocate x and y cell
x=cell(numtraj,1);y=cell(numtraj,1);fn=cell(numtraj,1);
%read each excelfile
for i=1:numtraj
xlsfilename = excelfiles(i).name; %current excel filename
pathtoexcelfile = strcat(folder_name,filesep,xlsfilename);
xRange = 'H:H';
yRange = 'I:I';
fnRange = 'B:B'; %fn=frame number
x{i}= xlsread(pathtoexcelfile,xRange);
y{i}= xlsread(pathtoexcelfile,yRange);
fn{i} = xlsread(pathtoexcelfile,fnRange);
end
%% plot excel file
for j=1:numtraj
    figure()
    plot(x{j},y{j},'--or'); hold on
    title(strcat('excel plot',num2str(j)));
    xlabel('x axis');
    ylabel('y axis');
end
%% read image file
numframe = length(tifFiles);
%preallocate tif cell
tif = cell(numframe,1);
%read each tif file.
for k=1:numframe
    tiffilename = tifFiles(k).name;
    pathtotiffile = strcat(folder_name,filesep,tiffilename);
    tif{k} = imread(pathtotiffile);
end
%% fill up empty frames with fake zeros
%preallocate new X and Y
X=cell(numtraj,1); Y=cell(numtraj,1);
%detect empty region, make zeros with the size, and attach to empty region
for n=1:numtraj
    if fn{n}(1)==1 %the front is not empty
        if fn{n}(length(fn{n}))==numframe %the tail is not empty
            %do nothing
        else %the tail is empty
            zerovec = zeros(numframe-length(fn{n}),1); %create empty tail length zeros
            X{n} = vertcat(x{n},zerovec); %add zeros to the tail
            Y{n} = vertcat(y{n},zerovec);
        end
    else fn{n}(1)~=1; %the front is empty   
        zerovec = zeros((fn{n}(1)-1),1); %vertical vector
        X{n} = vertcat(zerovec,x{n});
        Y{n} = vertcat(zerovec,y{n});
        if fn{n}(length(fn{n}))==numframe %the tail is not empty
            %do nothing
        else %the tail is empty
            zerovec = zeros((numframe-length(fn{n})-length(zerovec)),1); %create empty tail length zeros
            X{n} = vertcat(x{n},zerovec); %add zeros to the tail
            Y{n} = vertcat(y{n},zerovec);
        end
    end
end

%%


