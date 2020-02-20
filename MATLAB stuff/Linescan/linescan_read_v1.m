clear;clc;format short g;close all
%% user input variables
imageID = 2; 
Lend = 50; % default = 100
Rend = 900; % default = 900
minheight = 7000; % default = 7000 filter false peak
%7,10 have peaks at the very end -> adjust lend, rend
%13 have high false peak -> reduce minheight to 5000
%% read excel data
%19,20 is trouble
[num,txt,all] = xlsread('linescan_data.xlsx');
idx = imageID+imageID-1;
rawx=num(:,idx);
rawy=num(:,idx+1);
y=smoothdata(rawy);
%% cut off ends
% [Lpkx,Llocs]=findpeaks(y(1:200));
% Lend = Llocs(1);
% [Rpkx,Rlocs]=findpeaks(y(100:end));
% Rend = Rlocs(end);
y = y(Lend:Rend);
x = rawx(Lend:Rend);
%% find peaks
[pkx,locs,w,p]=findpeaks(y,...
    'MinPeakDistance',100,...
    'MinPeakProminence',1000);
if isempty(pkx)
    disp('no data in the excel')
    disp('check the excel sheet')
end
for i = 1:length(locs)
    leftw = locs(i)-w(i);
    rightw = locs(i)+w(i);
    realpkx(i) = max(rawy(Lend+leftw:Lend+rightw));
    reallocs(i) = find(rawy==realpkx(i));
end
rm = find(realpkx<minheight);
realpkx(rm)=[];
reallocs(rm)=[];
%% find avg value of flat areas
avg=zeros(1,length(locs)+1);
avgidx=zeros(1,length(locs)+1);
avg(1)=mean(y(1:locs(1)-w(1)));
avgidx(1)=(locs(1)-w(1)-0)/2+Lend;
if length(locs)==1 % #pk=1
    avg(2)=mean(y(locs(1)+w(1):end));
    avgidx(2)=(locs(1)+w(1))+(length(y)-(locs(1)+w(1)))/2+Lend;
end
if length(locs)==2 % #pk=2
    avg(2)=mean(y(locs(1)+w(1):locs(2)-w(2)));
    avgidx(2)=(locs(1)+w(1))+((locs(2)-w(2))-(locs(1)+w(1)))/2+Lend;
    avg(3)=mean(y(locs(2)+w(2):end));
    avgidx(3)=(locs(2)+w(2))+(length(y)-(locs(2)+w(2)))/2+Lend;
end
if length(locs)==3 % #pk=3
    avg(2)=mean(y(locs(1)+w(1):locs(2)-w(2)));
    avgidx(2)=(locs(1)+w(1))+((locs(2)-w(2))-(locs(1)+w(1)))/2+Lend;
    avg(3)=mean(y(locs(2)+w(2):end));
    avgidx(3)=(locs(2)+w(2))+((locs(3)-w(3))-(locs(2)+w(2)))/2+Lend;
    avg(4)=mean(y(locs(3)+w(3):end));
    avgidx(4)=(locs(3)+w(3))+(length(y)-(locs(3)+w(3)))/2+Lend;
end
%% plot result
figure(2)
%signal
plot(rawx,rawy);hold on
plot(x,y);hold on
%peak on raw
scatter(reallocs,realpkx);hold on
%flat avg
scatter(avgidx,avg);hold on
for i=1:length(reallocs)
    line([reallocs(i)-w(i) reallocs(i)-w(i)], get(gca, 'ylim'),'Color','red','LineStyle','--');
    line([reallocs(i)+w(i) reallocs(i)+w(i)], get(gca, 'ylim'),'Color','red','LineStyle','--');
end
disp('peak values are')
disp(realpkx')
disp('flat average values are')
disp(avg')


