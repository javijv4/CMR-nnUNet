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
conda install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu115
```
3. Install NNUNet: 
```
python -m pip install nnunetv2
```
4. Clone the CMR-nnUNet repository
```
git clone https://github.com/javijv4/CMR-nnUNet.git
```
