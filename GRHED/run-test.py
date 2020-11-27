# LIBRARY_PATH=/usr/local/cuda/lib64
import os
import sys
import argparse
import tensorflow as tf
from hed.utils.io import IO
from hed.test_example import HEDTester

import cv2
import numpy as np


def get_session(gpu_fraction):

    '''Assume that you have 6GB of GPU memory and want to allocate ~2GB'''

    num_threads = int(os.environ.get('OMP_NUM_THREADS'))
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_fraction)

    if num_threads:
        return tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, intra_op_parallelism_threads=num_threads))
    else:
        return tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))


    
def main(args):
    session = get_session(args.gpu_limit)
    tester = HEDTester(args.config_file,args.number_iterations,args.path_to_test_image)
    print("initialize")
    tester.setup(session)
    tester.run(session)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Utility for Training/Testing DL models(Concepts/Captions) using theano/keras')
    parser.add_argument('--config-file', dest='config_file', type=str, help='Experiment configuration file')
    parser.add_argument('--test-snapshot', dest='number_iterations', type=int, help='number of iterations for the pretrained model')
    parser.add_argument('--test-image', dest='path_to_test_image', type=str, help='path to the test image')
    parser.add_argument('--gpu-limit', dest='gpu_limit', type=float, default=1.0, help='Use fraction of GPU memory (Useful with TensorFlow backend)')
    args = parser.parse_args()
    main(args)
