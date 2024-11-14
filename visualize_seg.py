#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
Created on 2024/11/04 17:00:09

@author: Javiera Jilberto Vallejos 
'''

import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

img = nib.load('la_test_data/LA_4CH.nii')
seg = nib.load('la_test_data/la_4ch_seg.nii.gz')
png_fldr = 'la_test_data/pngs'

img_data = img.get_fdata()
seg_data = seg.get_fdata()

for i in range(img_data.shape[-1]):
    plt.figure(figsize=(10, 10))
    plt.imshow(img_data[:, :, 0, i], cmap='gray')
    
    # Create a copy of the segmentation data with transparency where the value is 0
    seg_display = np.ma.masked_where(seg_data[:, :, 0, i] == 0, seg_data[:, :, 0, i])
    
    plt.imshow(seg_display, cmap='jet', alpha=0.5)
    plt.axis('off')
    plt.title(f'Time Frame {i}')
    plt.savefig(f'{png_fldr}/screenshot_{i}.png', bbox_inches='tight')
    plt.close()