close all
clear all
clc
%load your own data and name it as noisy; 
    %noisy = imread(filename)
    noisy = double(im2gray(noisy));
    I=noisy;
    [M_data,N_data]=size(noisy);
    data_final=zeros(M_data,N_data,6);
    for alpha=1:6
       [magnitude,orientation,grady_I,gradx_I]=mexgrad(I,alpha);
       data_final(:,:,alpha)=magnitude;
    end
    noisy=data_final;

    savepath_1='test_mat_speckle/1look_123456_real/';
    savepath_2='real_image';
    savepath_3='.mat';
    savepath=strcat(savepath_1,savepath_2,savepath_3);
    save(savepath,'noisy','-v6');
% put the path of the data into a .lst file and replace the .lst file in --config-file for test data with this one.
