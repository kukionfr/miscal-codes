%Name: Kyu Sang Han 
%This is a practice 02 for reading excel and plot the points on TIF.
close all; clear; clc; 
%% read excel file
filename = 'Sheet1.xlsx';
%read first z=33~59 
x1Range = 'H2:H28';
y1Range = 'I2:I28';
fn1Range = 'B2:B28'; %fn=frame number
x1= xlsread(filename,x1Range);
y1= xlsread(filename,y1Range);
fn1 = xlsread(filename,fn1Range);
%read second z=33~59 
x2Range = 'H29:H55';
y2Range = 'I29:I55';
fn2Range = 'B29:B55';
x2 = xlsread(filename,x2Range);
y2 = xlsread(filename,y2Range);
fn2 = xlsread(filename,fn2Range);
%read third z=1~8 
x3Range = 'H56:H63';
y3Range = 'I56:I63';
fn3Range = 'B56:B63';
x3 = xlsread(filename,x3Range);
y3 = xlsread(filename,y3Range);
fn3 = xlsread(filename,fn3Range);
%% plot excel file
plot(x1,y1,'--or'); hold on
title('first excel plot');
xlabel('x axis');
ylabel('y axis');
axis([125,210,240,330])
figure()
plot(x2,y2,'--or'); hold on
title('second excel plot');
xlabel('x axis');
ylabel('y axis');
axis([125,210,240,330])
figure()
plot(x3,y3,'--or'); hold on
title('third excel plot');
xlabel('x axis');
ylabel('y axis');
axis([125,210,240,330])
%% adjust x and y to add empty frame's fake zero
emptyf1= zeros(fn1(1)-1,1);
x1 = vertcat(emptyf1,x1); x{1}=x1;
y1 = vertcat(emptyf1,y1); y{1}=y1;
emptyf2= zeros(fn2(1)-1,1);
x2 = vertcat(emptyf2,x2); x{2}=x2;
y2 = vertcat(emptyf2,y2); y{2}=y2;
emptyf3= zeros(59-8,1);
x3 = vertcat(x3,emptyf3); x{3}=x3;
y3 = vertcat(y3,emptyf3); y{3}=y3;
%% load images
for a=1:3
    tempx=x{a}; tempy=y{a};
count=0; %preallocate for loop count
for i=1:59
filename = ['t',num2str(i+187),'z6c3.tif'];
im = imread(filename); %read frame
figure(); 
imshow(im,[min(im(:)) max(im(:))]); axis([125,210,240,330]); axis on; colormap hot; hold on; %display frame
t=1; bigflag=0; %preallocate bigflag variable
while tempx(i) ~= 0 && tempy(i) ~= 0 && bigflag<t;
    k=i-33; flag=0;  
    if count > 32;
        while i-k>0 && flag<k;
            plot(tempx(i-k:i-1),tempy(i-k:i-1),'--or'); %accumulate from fn33
            axis([125,210,240,330]); hold on; %accumulate trajectory  
            flag=k+1;
        end
    end 
    %% special case for traj 3
    if a==3
        plot (tempx(1:i-1),tempy(1:i-1),'--or'); %accumulate from fn1
    end
    if count~=59;
        plot(tempx(i),tempy(i),'--or'); axis([125,210,240,330]); %overlay trajectory
    end
    bigflag=t+1;
end
new_filename = ['t', num2str(i+187), 'z6c3overlay.tif']; %name new file
saveas(figure(i+3),new_filename) %save overlaid images
temp1 = imread(new_filename);
f(i) = im2frame(temp1); %convert image into movie frame
count=i;
end
%% create tracking movie
figure()
axis tight manual
movie(f,1,4)
moviename=['overlaid',num2str(a),'.avi'];
movie2avi(f, moviename, 'fps', 4 , 'compression', 'None'); %create avi
close (4:63) 
end
close all

