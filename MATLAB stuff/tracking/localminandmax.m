% this function finds a local min of data in vector
function [Maxima, MaxIdx, Minima, MinIdx]=localminandmax(Data);
[Maxima,MaxIdx] = findpeaks(Data);
DataInv = 1.01*max(Data) - Data;
[Minima,MinIdx] = findpeaks(DataInv);
Minima=Data(MinIdx);
end