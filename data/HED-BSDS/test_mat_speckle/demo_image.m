close all
clear all
clc
load('1look_natural/112090.mat')
mean_value=mean(noisy(:));
std_value=std(noisy(:));
max_value=mean_value+3.0*std_value;
min_value=min(noisy(:));
noisy(noisy>max_value)=max_value;
I=(noisy-min_value)/(max_value-min_value);
figure,imshow(I)

load('1look_123456_natural/112090.mat')
image_data=noisy;
for ix=1:6
noisy=image_data(:,:,ix);
mean_value=mean(noisy(:));
std_value=std(noisy(:));
max_value=mean_value+3.0*std_value;
min_value=min(noisy(:));
noisy(noisy>max_value)=max_value;
I=(noisy-min_value)/(max_value-min_value);
figure,imshow(I)
end
