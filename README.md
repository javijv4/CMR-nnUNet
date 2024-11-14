# CMR-nnUNet
Scripts and models to run [nnUNet](https://github.com/MIC-DKFZ/nnUNet) inference on CMR images.

## Installation
To install the required packages to run the inference, first create a virtual environment. Here are the steps to create a conda environment, but it should be also possible to use venv.
1. Create and activate environment (you can call it whatever, here is called cmrnn)
```
conda create -n cmrnn 
conda activate cmrnn
```
2. Install PyTorch. Run the command indicated for your system [here](https://pytorch.org/get-started/locally/). In bigblue this command is 
```
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```
3. Install NNUNet: 
```
python -m pip install nnunetv2
```
NOTE: the current NNUNet has missing dependencies. You'll need to install them manually using:
```
python -m pip install blosc2 acvl_utils==0.2
```
4. Clone the CMR-nnUNet repository
```
git clone https://github.com/javijv4/CMR-nnUNet.git
```


## Installing pretrained models from .zip files
Make sure you downloaded the .zip files to the models folder. DATASET_NAME can be SA, LA_2CH, LA_3CH, LA_4CH.
```
nnUNetv2_install_pretrained_model_from_zip models/nn_DATASET_NAME.zip
```


## Running inference
Make sure you have installed the models you want to use (see above).
1. Modify the `run.sh` file according to the model you need. You need to set the `mode`, `id`, and `name` variables to one of these combinations
* SA, 41, 3d_fullres
* LA_2CH, 42, 2d
* LA_3CH, 43, 2d
* LA_4CH, 44, 2d
2. Run inference (make sure the conda environment is activated!)
```
bash run.sh
```
This will create a `name_seg.nii.gz` containing the segmentation. 