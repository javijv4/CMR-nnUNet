# CMR-nnUNet
Scripts and models to run [nnUNet](https://github.com/MIC-DKFZ/nnUNet) inference on CMR images.

## Installation
First, create a Python environment to install the required packages to run the inference. Here are the steps to create a conda environment, but it should also be possible to use venv. If you need to install conda, I recommend installing Miniconda, which is a lightweight version of Anaconda. You can find steps to install it in this [link](https://docs.anaconda.com/miniconda/install/#quick-command-line-install).
1. Create and activate environment (you can call it whatever, here is called cmrnn)
```
conda create -n cmrnn python=3.12
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
5. Set up paths. This step tells the NNUNet where to find and store the models and data that it needs. Detailed instructions on how to do this can be found [here](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/set_environment_variables.md). For a summary, do the following:
a. Create a folder for the NNUNet.
b. Set up paths:
* In Linux and MacOS: run the following commands in the terminal (temporal solution) or add them to your .bashrc (Linux) or .zshrc (Max).
```
export nnUNet_raw="path_to_NNUNet_fldr/nnUNet_raw"
export nnUNet_preprocessed="path_to_NNUNet_fldr/nnUNet_preprocessed"
export nnUNet_results="path_to_NNUNet_fldr/nnUNet_results"
```
* In Windows: follow the steps described for Windows [here](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/set_environment_variables.md).   


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
