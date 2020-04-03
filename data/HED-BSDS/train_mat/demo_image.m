load('train_image/1look_123456/train_image_10.mat')
for ix=1:6
noisy=image_data(:,:,ix);
mean_value=mean(noisy(:));
std_value=std(noisy(:));
val_max=mean_value+3.0*std_value;
noisy(noisy>val_max)=val_max;
min_value=min(noisy(:));
I=(noisy-min_value)/(val_max-min_value);
figure,imshow(I)
end

load('train_image/1look_image/train_image_10.mat')
noisy=image_data;
mean_value=mean(noisy(:));
std_value=std(noisy(:));
val_max=mean_value+3.0*std_value;
noisy(noisy>val_max)=val_max;
min_value=min(noisy(:));
I=(noisy-min_value)/(val_max-min_value);
figure,imshow(I)

