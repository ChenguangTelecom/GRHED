
close all
clear all
clc
path_data='temp_field/testing-example-6.mat';
%path_data='temp_1/testing-0-006.mat';
load(path_data)
for threshold=0.55
%add the path to the structured edge code
addpath(genpath('/data/cheliu/2018-2019/Desktop/edges-master'));
%add the path to the Piotr's matlab toolbox
addpath(genpath('/data/cheliu/2018-2019/Desktop/piotr_toolbox/toolbox'));

%Non-maxima suppression step defined in structured edge, and thresholding
[field_01,nms_01,map_01]=edgenms(magnitude_field,threshold);

figure,imshow(map_01)
end
