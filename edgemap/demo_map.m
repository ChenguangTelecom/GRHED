
close all
clear all
clc

path_1='GRHED-test/testing-';
path_end='-006.mat';
write_1='GRHED_map/image_1_';

%put the total number of images

for ix_image=0:7
index_image=int2str(ix_image);
path_data=strcat(path_1,index_image,path_end);

% gradient magnitude larger than threshold is edge pixel, and noise pixel otherwise

for threshold=0.45
%add the path to the structured edge code
addpath(genpath('/data/cheliu/2018-2019/Desktop/edges-master'));
%add the path to the Piotr's matlab toolbox
addpath(genpath('/data/cheliu/2018-2019/Desktop/piotr_toolbox/toolbox'));

%Non-maxima suppression step defined in structured edge, and thresholding
[field_01,nms_01,map_01]=edgenms(path_data,threshold);

figure,imshow(map_01)
write_path=strcat(write_1,index_image,'.png');
imwrite(map_01,write_path)
end
end
