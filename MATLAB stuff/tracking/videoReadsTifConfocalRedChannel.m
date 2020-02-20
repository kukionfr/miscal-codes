images=uigetdir;
jpegFiles = dir(strcat(images,'\*z6c3.tif'));
S = [jpegFiles(:).datenum]; 
[S,S] = sort(S);
jpegFilesS = jpegFiles(S);
% Image folder to -images-
VideoFile=strcat(images,'\RedChannel 20 fps z6c3');
writerObj = VideoWriter(VideoFile);

fps= 20; 
writerObj.FrameRate = fps;
open(writerObj);

for t= 1:length(jpegFilesS)
     Frame=imread(strcat(images,'\',jpegFilesS(t).name));
     
     % Eliminate this line if Frame comes in the uint8 format
     
     
     
     Frame = imadjust(Frame);
     Frame = uint8(Frame ./ 256);
     % RGB
     [a, b] = size(Frame);
     BlueGreen = zeros(a,b); 
     Frame = cat(3, Frame, BlueGreen, BlueGreen);
     %Frame=imadjust(Frame);
     
     
     writeVideo(writerObj,im2frame(Frame));
end

close(writerObj);

fprintf('done')