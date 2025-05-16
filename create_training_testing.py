#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
Created on 2024/11/03 10:38:20

@author: Javiera Jilberto Vallejos 
'''

import os

import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

import glob
import shutil

from tqdm import tqdm

# USER INPUTS
scans_fldr = 'nn_data'
datasets_fldr = 'datasets'
dump_png = False

views = ['4CH']


# Generate training and testing folders for each view
for view in views:
    print(f'Processing view {view}...')

    # Create view folder in NN-data
    if not os.path.exists(f'{datasets_fldr}/{view}'):
        os.makedirs(f'{datasets_fldr}/{view}')

    labels = [0, 1, 2, 3]
    if view == '2CH':
        labels = [0, 1, 2]

    # Grab all patient folders in LA-JAM
    patient_fldrs = glob.glob(scans_fldr + '/scan*')
    nn_patient_fldrs = []
    for patient_fldr in tqdm(patient_fldrs):
        # Grab patient number from patient folder
        patient_num = ''.join(filter(str.isdigit, patient_fldr.split('/')[-1]))
        patient_num = int(patient_num) + 1

        # Grab all nifti files in patient folder
        img_files = glob.glob(f'{patient_fldr}/{view}.nii.gz')
        img_files += glob.glob(f'{patient_fldr}/{view}.nii')
        seg_files = glob.glob(f'{patient_fldr}/{view}_seg.nii.gz')
        seg_files += glob.glob(f'{patient_fldr}/{view}_seg.nii')

        # If there are no files, skip the patient
        if len(img_files) == 0 or len(seg_files) == 0:
            continue

        # Check that the length of img_files and seg_files is 1
        if len(img_files) != 1 or len(seg_files) != 1:
            print(f'Error in patient folder: {patient_fldr}')
            print(f'img_files: {img_files}')
            print(f'seg_files: {seg_files}')
            continue

        # print(f'Processing patient {patient_num}...')

        # Create patient folder in NN-data if it doesn't exist
        patient_folder_path = f'{datasets_fldr}/{view}/patient{patient_num:03}'
        os.makedirs(patient_folder_path, exist_ok=True)

        # Read nifti files
        img = nib.load(img_files[0])
        seg = nib.load(seg_files[0])

        # Save img in NN-data patient folder
        nib.save(img, f'{datasets_fldr}/{view}/patient{patient_num:03}/patient{patient_num:03}_4d.nii.gz')

        seg_data = seg.get_fdata()
        img_data = img.get_fdata()

        # Check that seg_data only contains 0, 1, 2, 3
        seg_labels = np.round(np.unique(seg_data)).astype(int)
        if len(seg_labels) != len(labels):
            print(f'Error in patient folder: {patient_fldr}')
            print(f'Unique values in seg_data: {seg_labels}')
            continue
        if not np.all(seg_labels == labels):
            print(f'Error in patient folder: {patient_fldr}')
            print(f'Unique values in seg_data: {np.unique(seg_data)}')
            continue

        # Check that the number of frames is the same in img and seg
        if seg_data.shape[-1] != img_data.shape[-1]:
            print(f'Error in patient folder: {patient_fldr}')
            print(f'seg_data.shape: {seg_data.shape}')
            print(f'img_data.shape: {img_data.shape}')
            continue

        # Check what frames in seg are non-zero
        nframes = seg_data.shape[-1]
        sum_frames = np.sum(seg_data.reshape(-1, nframes), axis=0)
        frames = np.where(sum_frames > 0)[0]

        # # If there are also multiple frames in z, check which one has data and collapse the z dimension
        # # TODO: I should check this is consecutive frames
        # if seg_data.shape[2] > 1:
        #     aux = seg_data[..., frames[0]]
        #     sum_slices = np.sum(aux.reshape(-1, seg_data.shape[2]), axis=0)
        #     slices = np.where(sum_slices > 0)[0]
        #     # if len(slices) > 1:
        #     #     slices = slices[0]
        #     seg_data = seg_data[:, :, slices, :]
        #     img_data = img_data[:, :, slices, :]

        # Check there are only two frames
        if len(frames) != 2:
            print(f'Patient folder: {patient_fldr} has {len(frames)} frames')
            print(f'frames: {frames}')
        
        # Save the frames and gt in NN-data patient folder
        for frame in frames:
            seg_frame = seg_data[..., frame]
            img_frame = img_data[..., frame]

            if view == 'SA':
                # Save all frames
                seg_frame = nib.Nifti1Image(seg_frame, np.eye(4))
                nib.save(seg_frame, f'{datasets_fldr}/{view}/patient{patient_num:03}/patient{patient_num:03}_frame{frame+1:02}_gt.nii.gz')

                # Save img frame
                img_frame = nib.Nifti1Image(img_frame, np.eye(4))
                nib.save(img_frame, f'{datasets_fldr}/{view}/patient{patient_num:03}/patient{patient_num:03}_frame{frame+1:02}.nii.gz')

            else:    # 2D data
                # Check what slices have data
                slices = np.where(np.sum(seg_frame, axis=(0, 1)) > 0)[0]
                for slice in slices:
                    seg_frame_slice = np.round(seg_frame[..., slice])
                    img_frame_slice = np.round(img_frame[..., slice])

                    # Save seg frame
                    seg_nii = nib.Nifti1Image(seg_frame_slice, np.eye(4))
                    nib.save(seg_nii, f'{datasets_fldr}/{view}/patient{patient_num:03}/patient{patient_num:03}_frame{frame+1:02}_slice{slice+1:02}_gt.nii.gz')

                    # Save img frame
                    img_nii = nib.Nifti1Image(img_frame_slice, np.eye(4))
                    nib.save(img_nii, f'{datasets_fldr}/{view}/patient{patient_num:03}/patient{patient_num:03}_frame{frame+1:02}_slice{slice+1:02}.nii.gz')


            if dump_png:
                # Plot img with seg overlay and save image to patient folder

                fig, ax = plt.subplots(1, 1, figsize=(8, 8))
                ax.imshow(img_frame.get_fdata(), cmap='gray')
                
                # Use transparency and jet colormap for the segmentation
                seg_overlay = np.ma.masked_where(seg_frame.get_fdata() == 0, seg_frame.get_fdata())
                ax.imshow(seg_overlay, cmap='jet', alpha=0.5)
                
                ax.axis('off')

                plt.savefig(f'{datasets_fldr}/{view}/patient{patient_num:03}/patient{patient_num:03}_frame{frame+1:02}_overlay.png', bbox_inches='tight', pad_inches=0)
                plt.close(fig)

        nn_patient_fldrs.append(patient_folder_path)

    print(f'Found {len(nn_patient_fldrs)} patients in {datasets_fldr}/{view}')

    # Split the patient folders into training and testing
    np.random.seed(42)
    np.random.shuffle(nn_patient_fldrs)

    train_fldrs = nn_patient_fldrs[:int(0.8*len(nn_patient_fldrs))]
    test_fldrs = nn_patient_fldrs[int(0.8*len(nn_patient_fldrs)):]
    print(f'Training folders ({len(train_fldrs)}): {train_fldrs}')
    print(f'Testing folders ({len(test_fldrs)}): {test_fldrs}')

    # Create training and testing folders in NN-data
    os.makedirs(f'{datasets_fldr}/{view}/training', exist_ok=True)
    os.makedirs(f'{datasets_fldr}/{view}/testing', exist_ok=True)

    # Move training and testing folders
    for train_fldr in train_fldrs:
        shutil.move(train_fldr, f'{datasets_fldr}/{view}/training/')

    for test_fldr in test_fldrs:
        shutil.move(test_fldr, f'{datasets_fldr}/{view}/testing/')

    print('Done!')