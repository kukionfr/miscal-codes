clear;clc;format short g;close all
%% read excel data
[num,txt,all] = xlsread('linescan_data.xlsx');
imgs = txt(1,:);
rawx=num(:,1);
rawy=num(:,2);
y=smoothdata(rawy);
%% find peaks
[pkx,locs,w,p]=findpeaks(y,...
    'MinPeakDistance',100,...
    'MinPeakProminence',1000);
% %% cut off by histogram
% LE=y(1:locs(1)-w(1));
% plot(y);hold on
% plot(LE);
% [count,bin]=hist(LE,100);
% figure;bar(bin,count);
% mode=bin(find(count==max(count)));
% figure;plot(bin,count)
% for i=fliplr(1:length(LE))
%     if y(i)>mode+500 && 
% end

%% find avg value of flat areas
% avg=zeros(1,length(locs)+1);
% avgidx=zeros(1,length(locs)+1);
% avg(1)=mean(y(1:locs(1)-w(1)));
% avgidx(1)=(locs(1)-w(1)-0)/2+Lend;
% if length(locs)==1 % #pk=1
%     avg(2)=mean(y(locs(1)+w(1):end));
%     avgidx(2)=(locs(1)+w(1))+(length(y)-(locs(1)+w(1)))/2+Lend;
% end
% if length(locs)==2 % #pk=2
%     avg(2)=mean(y(locs(1)+w(1):locs(2)-w(2)));
%     avgidx(2)=(locs(1)+w(1))+((locs(2)-w(2))-(locs(1)+w(1)))/2+Lend;
%     avg(3)=mean(y(locs(2)+w(2):end));
%     avgidx(3)=(locs(2)+w(2))+(length(y)-(locs(2)+w(2)))/2+Lend;
% end
% if length(locs)==3 % #pk=3
%     avg(2)=mean(y(locs(1)+w(1):locs(2)-w(2)));
%     avgidx(2)=(locs(1)+w(1))+((locs(2)-w(2))-(locs(1)+w(1)))/2+Lend;
%     avg(3)=mean(y(locs(2)+w(2):end));
%     avgidx(3)=(locs(2)+w(2))+((locs(3)-w(3))-(locs(2)+w(2)))/2+Lend;
%     avg(4)=mean(y(locs(3)+w(3):end));
%     avgidx(4)=(locs(3)+w(3))+(length(y)-(locs(3)+w(3)))/2+Lend;
% end
% %% plot result
% figure(2)
% %signal
% plot(rawx,rawy);hold on
% plot(x,y);hold on
% %peak on raw
% scatter(locs+Lend-1,rawy(locs+Lend-1));hold on
% %peak on smooth
% scatter(locs+Lend-1,y(locs));hold on
% %flat avg
% scatter(avgidx,avg);hold on
% for i=1:length(locs)
%     line([locs(i)-w(i)+Lend locs(i)-w(i)+Lend], get(gca, 'ylim'),'Color','red','LineStyle','--');
%     line([locs(i)+w(i)+Lend locs(i)+w(i)+Lend], get(gca, 'ylim'),'Color','red','LineStyle','--');
% end
% disp('peak values are')
% disp(pkx)
% disp('flat average values are')
% disp(avg')
% 
% 
