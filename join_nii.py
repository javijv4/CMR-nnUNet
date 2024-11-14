#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 10:11:36 2023

@author: Javiera Jilberto Vallejos
"""
import numpy as np
import nibabel as nib
import glob
import sys

if len(sys.argv) > 1:
    path = sys.argv[1]
    file_name = sys.argv[2]
else:
    path = 'test_data/'
    file_name = '2CH'

seg_fldr = 'segs/'

files = glob.glob(path + seg_fldr + '*.nii.gz')
files = list(np.sort(files))

nframes = len(files)

# Read first to get data size
img = nib.load(files[0])
data_fr = img.get_fdata()

data = np.zeros([*data_fr.shape, nframes], dtype=int)
data[:,:,:,0] = data_fr

for i, file in enumerate(files[1:]):
    fr = i+1
    img = nib.load(file)
    data_fr = img.get_fdata()
    data[:,:,:,fr] = data_fr

new_img = nib.Nifti1Image(data, img.affine, header=img.header)
nib.save(new_img, path + file_name + '_seg.nii.gz')