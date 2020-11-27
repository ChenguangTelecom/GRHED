import os
from os.path import isdir
import sys
import argparse
import yaml
import urlparse
import urllib
import StringIO
import cStringIO
import numpy as np
from PIL import Image
import tensorflow as tf
import scipy.io as sio
import matplotlib.pyplot as plt
import cv2
import numpy as np
#import matlab.engine
#eng=matlab.engine.start_matlab()


from hed.models.vgg16 import Vgg16
from hed.utils.io import IO


def show_image(img):
    min_value=np.min(img)
    mean_value=np.mean(img)
    std_value=np.std(img)
    max_value=mean_value+3.0*std_value
    img[img>max_value]=max_value
    img=(img-min_value)/(max_value-min_value)
    plt.imshow(img)

def kernel_generate(W,alpha):
    W=W.astype(int)
    alpha=alpha+0.0
    kernel_x_left=np.zeros((2*W+1,2*W+1),dtype=np.float32)
    kernel_x_right=np.zeros((2*W+1,2*W+1),dtype=np.float32)
    kernel_y_up=np.zeros((2*W+1,2*W+1),dtype=np.float32)
    kernel_y_bm=np.zeros((2*W+1,2*W+1),dtype=np.float32)
    for ix in range(2*W+1):
        for jx in range(W):
            kernel_x_left[ix,jx]=np.exp((-abs(ix-W)-abs(jx-W))/alpha)
            kernel_x_right[ix,2*W-jx]=np.exp((-abs(ix-W)-abs(W-jx))/alpha)
            kernel_y_up[jx,ix]=np.exp((-abs(jx-W)-abs(ix-W))/alpha)
            kernel_y_bm[2*W-jx,ix]=np.exp((-abs(W-jx)-abs(ix-W))/alpha)
    return kernel_x_left,kernel_x_right,kernel_y_up,kernel_y_bm


def compute_GR(img, alpha):
    img[img<1.0]=1.0
    alpha=alpha+0.0
    W=np.ceil(np.log(10.0)*alpha)
    kernel_x_left,kernel_x_right,kernel_y_up,kernel_y_bm=kernel_generate(W,alpha)

    gradx_left=cv2.filter2D(img,-1,kernel_x_left,borderType=cv2.BORDER_REPLICATE)
    gradx_right=cv2.filter2D(img,-1,kernel_x_right,borderType=cv2.BORDER_REPLICATE)
    grady_up=cv2.filter2D(img,-1,kernel_y_up,borderType=cv2.BORDER_REPLICATE)
    grady_bm=cv2.filter2D(img,-1,kernel_y_bm,borderType=cv2.BORDER_REPLICATE)
    
    ratio_x=np.divide(gradx_right,gradx_left)
    ratio_y=np.divide(grady_bm,grady_up)
    log_ratio_x=np.log(ratio_x)
    log_ratio_y=np.log(ratio_y)
    gradn=np.sqrt(np.square(log_ratio_x)+np.square(log_ratio_y))
    gradp=np.arctan2(log_ratio_y,log_ratio_x)
    return gradn, gradp


class HEDTester():

    def __init__(self, config_file,number_iterations,path_test_image):

        self.io = IO()
        self.init = True

        try:
            pfile = open(config_file)
            self.cfgs = yaml.load(pfile)
            pfile.close()

        except Exception as err:

            self.io.print_error('Error reading config file {}, {}'.format(config_file), err)

        try:
            self.test_snapshot=number_iterations
        except Exception as err:
           self.io.print_error('please choose an existing pretrained model')
        try:
            self.test_image=path_test_image
        except Exception as err:
            self.io.print_error('the chosen test image does not exist')
            
                

    def setup(self, session):

        try:

            self.model = Vgg16(self.cfgs, run='testing')

            meta_model_file = os.path.join(self.cfgs['save_dir'], 'models/hed-model-{}'.format(self.test_snapshot))

            saver = tf.train.Saver()
            saver.restore(session, meta_model_file)

            self.io.print_info('Done restoring VGG-16 model from {}'.format(meta_model_file))

        except Exception as err:

            self.io.print_error('Error setting up VGG-16 model, {}'.format(err))
            self.init = False

    def run(self, session):

        if not self.init:
            return

        self.model.setup_testing(session)
        test_filename = self.test_image
        im=sio.loadmat(test_filename)['noisy']
        new_im=im.astype(np.float32)
        MM,NN=np.shape(new_im)
        GR_n=np.zeros((MM,NN,6),dtype=np.float32)
        GR_p=np.zeros((MM,NN,6),dtype=np.float32)
        for alpha in range(1,7):
            GR_n[:,:,alpha-1], GR_p[:,:,alpha-1]=compute_GR(new_im,alpha)
        
        GR_n -= self.cfgs['mean_pixel_value']
        im=GR_n[:,:,1:5]
        edgemap = session.run(self.model.predictions, feed_dict={self.model.images: [im]})
       
        em_maps = [e[0] for e in edgemap]
        em_maps = em_maps + [np.mean(np.array(em_maps), axis=0)]
        plt.figure()
        for idx, em in enumerate(em_maps):
            em=np.squeeze(em)
            save_mat_dir='temp_field'
            if not isdir(save_mat_dir):
                os.makedirs(save_mat_dir)
             
            save_mat_path=os.path.join('temp_field', 'testing-example-{}'.format(idx))
            sio.savemat(save_mat_path,{'magnitude_field':em})

            #[field_01,nms_01,map_01]=eng.edgenms(em,0.45);
            
            
            #em=map_01
            #em[em < 0.45] = 0.0
            #show_image(em)
        #plt.show()
        #plt.close()

    

    
