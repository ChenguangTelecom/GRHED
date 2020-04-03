close all
clear all
clc

fid=fopen('test.txt');
data_name=textscan(fid,'%s');
fclose(fid);
hed_name=data_name{1};

fid_mat=fopen('test_1look_alpha_123456_natural.txt','wt');
formatSpec='%s\n';

fid_1look=fopen('test_1look_natural.txt','wt');
formatSpec='%s\n';
for ix=1:size(hed_name,1)
    ix
    c1=hed_name(ix);
    d1=c1{1};
    image_data_color=imread(d1);
    clean_image_data=double(rgb2gray(image_data_color));
    clean_image_data=imresize(clean_image_data,[320,480]);
    nlook=1;
    noisy=Noise(clean_image_data,nlook);
    I=noisy;
    [M_data,N_data]=size(noisy);
    data_final=zeros(M_data,N_data,6);
    for alpha=1:6
       [magnitude,orientation,grady_I,gradx_I]=mexgrad(I,alpha);
       data_final(:,:,alpha)=magnitude;
    end
    noisy=data_final;

    length_d1=length(d1);
  
    hed_file=d1(6:(length_d1-3));
    savepath_1='test_mat_speckle/1look_123456_natural/';
    savepath_2=hed_file;
    savepath_3='mat';
    savepath=strcat(savepath_1,savepath_2,savepath_3);
    save(savepath,'noisy','-v6');
    savepath=char(savepath);
    fprintf(fid_mat,formatSpec,savepath);


    noisy=I;
    hed_file=d1(6:(length_d1-3));
    savepath_1='test_mat_speckle/1look_natural/';
    savepath_2=hed_file;
    savepath_3='mat';
    savepath=strcat(savepath_1,savepath_2,savepath_3);
    save(savepath,'noisy','-v6');
    savepath=char(savepath);
 fprintf(fid_1look,formatSpec,savepath);

end
fclose(fid_mat)
fclose(fid_1look)
