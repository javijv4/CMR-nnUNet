#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 09:51:31 2023

@author: Javiera Jilberto Vallejos
"""

import nibabel as nib
import os
import sys

if len(sys.argv) > 1:
    path = sys.argv[1]
    file = sys.argv[2]
else:
    path = 'KL-5/'
    file = '2CH'


try: 
    img = nib.load(path + file + '.nii')
except:
    img = nib.load(path + file + '.nii.gz')
data = img.get_fdata()

if not os.path.exists(path + 'imgs/'):
    os.mkdir(path + 'imgs/')

assert len(data.shape) == 4
for fr in range(data.shape[-1]):
    new_img = nib.Nifti1Image(data[:,:,:,fr], img.affine, header=img.header)
    nib.save(new_img, path + 'imgs/' + file + '_%03i' % fr + '_0000.nii.gz')