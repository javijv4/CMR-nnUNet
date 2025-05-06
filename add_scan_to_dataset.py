#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
Created on 2025/05/06 15:28:21

@author: Javiera Jilberto Vallejos 
'''
import os
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
from tkinter import Tk, messagebox
from tkinter import font

scan_folder = 'HCM_pt1_Baseline'
nn_data_folder = 'raw_data/'
data_description = 'hcm_data/pt1_baseline'
scan_number = 118

imgs_name = {
    # 'SA': 'sa',
    '2CH': 'LA_2CH.nii.gz',
    '3CH': 'LA_3CH.nii.gz',
    '4CH': 'LA_4CH.nii.gz'
}

segs_name = {
    # 'SA': 'sa_seg',
    '2CH': 'la_2ch_seg_nn.nii.gz',
    '3CH': 'la_3ch_seg_nn.nii.gz',
    '4CH': 'la_4ch_seg_nn.nii.gz'
}

# First check: there is not a scan folder with the same name
if os.path.exists(f'{nn_data_folder}/scan{scan_number:03d}'):
    raise FileExistsError(f"Folder scan{scan_number:03d} already exists. Please choose a different number.")


for view in imgs_name.keys():
    img = nib.load(f'new_data/{scan_folder}/{imgs_name[view]}').get_fdata()
    seg = nib.load(f'new_data/{scan_folder}/{segs_name[view]}').get_fdata()


    frames = np.where(np.sum(seg, axis=(0, 1, 2)) > 0)[0]

    for frame in frames:
        slices = np.where(np.sum(seg[:, :, :, frame], axis=(0, 1)) > 0)[0]

        for slice_idx in slices:
            fig, ax = plt.subplots()

            # Display the image
            ax.imshow(img[:, :, slice_idx, frame], cmap='gray', origin='lower')

            # Overlay the segmentation with transparency
            segmentation = seg[:, :, slice_idx, frame]

            masked_seg = np.ma.masked_where(segmentation == 0, segmentation)
            ax.imshow(masked_seg, cmap='jet_r', alpha=0.4, origin='lower', vmin=1, vmax=3)

            # Add title and remove axes
            ax.set_title(f"{view.capitalize()}, Frame {frame}, Slice {slice_idx}\n"
                        "Did you check the base is a straight line? \n"
                        "Did you check there are no gaps between regions\n")
            ax.axis('off')


# Prompt the user with a yes/no question
plt.show()

# Create a hidden root window
root = Tk()
root.withdraw()
# Show the prompt with a custom font

response = messagebox.askyesno("Check", "Are the segmentations correct? \n"
"Are there only two frames in each view? \n", icon='question')

# # If the user clicks "Yes", save the figure
if response:

    response = messagebox.askyesno("Check", 
    f"Is the data description '{data_description}' correct for the scan folder '{scan_folder}'? \n", icon='question')

    if response:
        # Create output folder
        os.makedirs(f'{nn_data_folder}/scan{scan_number:03d}', exist_ok=True)

        # Save images
        for view in imgs_name.keys():
            img = nib.load(f'new_data/{scan_folder}/{imgs_name[view]}')
            seg = nib.load(f'new_data/{scan_folder}/{segs_name[view]}')

            nib.save(img, f'{nn_data_folder}/scan{scan_number:03d}/{view}.nii.gz')
            nib.save(seg, f'{nn_data_folder}/scan{scan_number:03d}/{view}_seg.nii.gz')


# Show a message box indicating success
messagebox.showinfo("Success", "The data was copied successfully.\n"
                    "Please remember to data in the new_data/ folder.")