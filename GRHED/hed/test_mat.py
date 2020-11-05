import os
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

from hed.models.vgg16 import Vgg16
from hed.utils.io import IO


class HEDTester():

    def __init__(self, config_file):

        self.io = IO()
        self.init = True

        try:
            pfile = open(config_file)
            self.cfgs = yaml.load(pfile)
            pfile.close()

        except Exception as err:

            self.io.print_error('Error reading config file {}, {}'.format(config_file), err)

    def setup(self, session):

        try:

            self.model = Vgg16(self.cfgs, run='testing')

            meta_model_file = os.path.join(self.cfgs['save_dir'], 'models/hed-model-{}'.format(self.cfgs['test_snapshot']))

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

        filepath = os.path.join(self.cfgs['download_path'], self.cfgs['testing']['list'])
        train_list = self.io.read_file_list(filepath)

        self.io.print_info('Writing PNGs at {}'.format(self.cfgs['test_output']))

        for idx, img in enumerate(train_list):

            test_filename = os.path.join(self.cfgs['download_path'], self.cfgs['testing']['dir'], img)
            im=sio.loadmat(test_filename)['noisy']
            #im=cv2.resize(im,(self.cfgs['testing']['image_height'], self.cfgs['testing']['image_width']))
        
            new_im=im.astype(np.float32)
            new_im -= self.cfgs['mean_pixel_value']
            im=new_im[:,:,1:5]
      
            #im=np.expand_dims(im,axis=2)

            edgemap = session.run(self.model.predictions, feed_dict={self.model.images: [im]})
            self.save_egdemaps(edgemap, idx)

            self.io.print_info('Done testing {}, {}'.format(test_filename, im.shape))

    def save_egdemaps(self, em_maps, index):

        # Take the edge map from the network from side layers and fuse layer
        em_maps = [e[0] for e in em_maps]
        em_maps = em_maps + [np.mean(np.array(em_maps), axis=0)]

        for idx, em in enumerate(em_maps):

            em[em < self.cfgs['testing_threshold']] = 0.0
            save_mat_path=os.path.join(self.cfgs['test_output'], 'testing-{}-{:03}'.format(index, idx))
            sio.savemat(save_mat_path,{'magnitude_field':em})

            em = 255.0 * (1.0 - em)
            
            em = np.tile(em, [1, 1, 3])

            em = Image.fromarray(np.uint8(em))
            em.save(os.path.join(self.cfgs['test_output'], 'testing-{}-{:03}.png'.format(index, idx)))

    

    
