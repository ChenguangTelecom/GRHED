function [ESM,ESM_nms,edgemap]=edgenms(path_data,threshold)
rr=1;
ss=5;
load(path_data)
E_hed=magnitude_field;
ESM=E_hed;

E_hed=single(E_hed);
[Ox,Oy]=gradient2(convTri(E_hed,4));
[Oxx,~]=gradient2(Ox); [Oxy,Oyy]=gradient2(Oy);
O=mod(atan(Oyy.*sign(-Oxy)./(Oxx+1e-5)),pi);
edgemap_hed=edgesNmsMex(E_hed,O,rr,ss,1.01,4);
ESM_nms=edgemap_hed;

imwrite(ESM_nms,'temp_map.png')
pb=double(imread('temp_map.png'))/255.0;
edgemap_hed=pb;
edgemap_hed(edgemap_hed>threshold)=1;
edgemap_hed(edgemap_hed<=threshold)=0;
edgemap=edgemap_hed;

