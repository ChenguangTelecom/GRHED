## GRHED, an edge detector for SAR images
This repository contains the implementation of paper GRHED [download](https://hal.archives-ouvertes.fr/hal-02424315/). 

version 1.1-March 20, 2020

by Chenguang Liu 

Email: chenguangl@whu.edu.cn


## NOTICE: 
The source code of GRHED is modified from the code (tensorflow implementation) of the paper Holistically-Nested Edge Detection (https://dl.acm.org/doi/10.5555/3158436.3158453). The code is hosted at 'https://github.com/moabitcoin/holy-edge'
and also hosted at `https://github.com/harsimrat-eyeem/holy-edge` - Harsimrat Sandhawalia

## 1. Generate 1-look simulated SAR images and compute their gradient magnitude fields using GR
step 1: You should download the clean image data according to the instructions in the link 'https://github.com/moabitcoin/holy-edge'. The command to download the clean data can also found below The clean image data should be in the folder 'data/HED-BSDS/'. The path to the clean training image should be located in 'data/HED-BSDS/train' and the path to the clean test image should be in 'data/HED-BSDS/test'.

step 2: After downloading the image, and put them in the right path, you should run demo_training_data.m located in 'data/HED-BSDS/' to generate the 1-look speckled optical images and their corresponding gradient magnitude fields computed by GR with alpha=1,2,3,4,5,6. Two .txt file containing the list of path to each speckled optical images and their gradient magnitude fields will be created: train_pair_mat_1look.txt and train_pair_mat_1look_alpha_123456.txt. Rename both .txt files to be .lst file.

step 3: After generating the data for training, we can train HED on the gradient magnitude fields.

Description of the folder 'data/HED-BSDS/':

train: folder of the clean training images.

test: folder of the clean testing images.

train_mat: path to the speckled optical images for training.

test_mat_speckle: path to the speckled optical images for testing.

train_pair.txt: list of path to the training data.

test.txt: list of path to the testing data.

train_pair_mat_1look.txt: list of path to the 1-look speckled optical images for training, you should save it as .lst file if you want to use it for training. 

train_pair_mat_1look_alpha_123456.lst: list of path to the gradient magnitude fields computed by GR with alpha=1,2,3,4,5,6, on the speckled optical images listed in train_pair_mat_1look.txt. 

test_1look_natural.txt: list of path to the 1-look speckled optical images for testing. 

test_1look_alpha_123456_natural.txt: list of path to the gradient magnitude fields computed by GR with alpha=1,2,3,4,5,6, on the speckled optical images listed in test_1look_natural.txt.

demo_training_data.m: the code to generate the 1-look images and their corresponding gradient magnitude fields for training, the .txt file containing the list of path will be generated at the same time.

demo_test_data.m: the code to generate the 1-look images and their corresponding gradient magnitude fields for testing, the .txt file containing the list of path will also be generated at the same time.

demo_test_real_data.m: the code used to generate the gradient magnitude fields of any testing data, simulated SAR images or real SAR images depending on your choice.

mexgrad.c: the mex code implementing gradient computation by GR, to compile it, please type the following command in matlab: 
mex mexgrad.c

Noise.m: multiplying a clean image with speckle noise. You can specify the number of looks for the speckle noise.

## 2. Training HED on the gradient magnitude fields.
Installing requirements with the following command:

cd GRHED

pip install -r requirements.txt

export OMP_NUM_THREADS=1

 Notice that, the original code as well as our implementation are based on python 2.7, but the code cab be modified to be executed on python3, if you do some modifications on print functin ..etc. 


You should edit the config file located at GRHED/hed/configs/hed.yaml to set the path of storing the clean image, the simulated SAR images and testing SAR images. You should also set the path storing the trained models and testing results. You can also set the hyperparameters for training.

hed-restore.yaml is the config file for continue training. You can set the path of pretrained models the path to save newly trained models, as well as hyperparameters.
The code is modified from the tensorflow implementation of HED in the link 'https://github.com/moabitcoin/holy-edge' 

You can consult the link 'https://github.com/moabitcoin/holy-edge' if you want to know more detailed description. However, there are several modifications in our code:

1. In our implementation, HED is trained from scratch, there is no need to download the pretrained weights of vgg16.

2. the input of the data to the network is .mat files.

3. we have a run-hed-restore.py and hed-restore.yaml for continue training.

After setting up, you can run the following command to download the clean augmented BSDS500 images:

export OMP_NUM_THREADS=1

python run-hed.py --download-data --config-file hed/configs/hed.yaml

After downloading, the path to the clean training images should be data/HED-BSDS/train.

## 3. Training
export CUDA_VISIBLE_DEVICES=0

export OMP_NUM_THREADS=1

python run-hed.py --train --config-file hed/configs/hed.yaml

You can continue to train HED from a pretrained models with the following command
python run-hed-restore.py --train --config-file hed/configs/hed-restore.yaml

## 4. Testing
You can contact me to ask for the pretrained models.

Choose a models trained with a certain number of iterations by setting 

test_snapshot: 

located in GRHED/hed/configs/hed.yaml and GRHED/hed/configs/hed-restore.yaml.

Then run 

export CUDA_VISIBLE_DEVICES=0

export OMP_NUM_THREADS=1

python run-hed.py --test --config-file hed/configs/hed.yaml

or run

export CUDA_VISIBLE_DEVICES=0

export OMP_NUM_THREADS=1

python run-hed-restore.py --test --config-file hed/configs/hed-restore.yaml

To better understanding the code of HED, please refer to 'https://github.com/moabitcoin/holy-edge'.

## 5. Postprocessing to obtain edge maps.
First copy the gradient magnitude fields computed by GRHED to the folder edgemap

cp -r GRHED-test edgemap/

cd edgemap

Then run demo_map.m to obtain the binary edge map with a certain threshold.
edgenms.m applies the Non-maxima suppression step used in Structured edge. To successfully run the code edgenms.m, you should download the code of structured edge from the link: 'https://github.com/pdollar/edges'. You should also download the Pitor' matlab toolbox from the link: https://pdollar.github.io/toolbox/

After downloading them, you should modify the path to them in demo_map.m

Then you should be able to obtain binary edge maps from the gradient magnitude fields computed by GRHED.

## If you have any questions, please feel free to contact me by email: chenguangl@whu.edu.cn
