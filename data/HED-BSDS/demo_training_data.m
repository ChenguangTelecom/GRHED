close all
clear all
clc
fid=fopen('train_pair.txt');
data=textscan(fid,'%s %s');
fclose(fid);
train_image=data{1};
train_gt=data{2};
path_train_image='train_mat/train_image/1look_123456/train_image_';
path_train_gt='train_mat/train_gt/train_gt_';

fid_mat=fopen('train_pair_mat_1look_alpha_123456.txt','wt');
formatSpec='%s %s\n';

path_train_image_1look='train_mat/train_image/1look_image/train_image_';

fid_1look=fopen('train_pair_mat_1look.txt','wt');
formatSpec='%s %s\n';

for ix=1:size(train_image,1)
ix
    index_ix=num2str(ix);
    type_image={'.mat'};
    image_path=strcat(path_train_image,index_ix,type_image);
    image_path_1look=strcat(path_train_image_1look,index_ix,type_image);
    gt_path=strcat(path_train_gt,index_ix,type_image);
    
    save_image_path=image_path;
    save_image_path_1look=image_path_1look;
    save_gt_path=gt_path;

    image_path=char(image_path);
    image_path_1look=char(image_path_1look);
    gt_path=char(gt_path);
    fprintf(fid_mat,formatSpec,image_path,gt_path);
    fprintf(fid_1look,formatSpec,image_path_1look,gt_path);

    str_train_image=char(train_image(ix));
    str_train_gt=char(train_gt(ix));
    image_data=imread(str_train_image);
    gt_data=imread(str_train_gt);
    if size(gt_data,3)>2
        gt_data=rgb2gray(gt_data);
    end


    image_path=save_image_path{1};
    image_path_1look=save_image_path_1look{1};
    gt_path=save_gt_path{1};
    image_data=double(rgb2gray(image_data));
  
    nlook=1;
    noisy_data=Noise(image_data,nlook);
    I=double(noisy_data);
    [msize,nsize]=size(noisy_data);
    image_data=zeros(msize,nsize,6);
    for alpha=1:6
       [magnitude,orientation,grady_I,gradx_I]=mexgrad(I,alpha);
       image_data(:,:,alpha)=magnitude;
    end
    save(image_path,'image_data','-v6');
    image_data=I;
    save(image_path_1look,'image_data','-v6');
    save(gt_path,'gt_data','-v6');
    
end
fclose(fid_mat);
fclose(fid_1look);
