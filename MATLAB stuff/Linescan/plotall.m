[num,txt,all] = xlsread('linescan_data.xlsx');
cla;
for i=1:length(num(1,:))/2
    figure(1)
    rawx=num(:,(i-1)*2+1);
    rawy=num(:,i*2);
    rawy=rawy/max(rawy)+1.2*i;
    plot(rawx,rawy); hold on;
end