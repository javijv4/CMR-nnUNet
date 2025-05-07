#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
Created on 2025/04/02 09:12:58

@author: Javiera Jilberto Vallejos 
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import nibabel as nib

from tqdm import tqdm
import csv

from glob import glob

views = ['sa', '2ch', '3ch', '4ch']

folders = glob('nn_data/scan*')
folders = sorted(folders, key=lambda x: int(x[-3:]))

with PdfPages('nn_data/output_images.pdf') as pdf:
    for scan_fldr in tqdm(folders):
        i = int(scan_fldr[-3:])

        imgs = {}
        segs = {}
        seg_found = 0
        img_found = 0
        label_found = {}
        for view in views:
            img_path = f'{scan_fldr}/{view.upper()}.nii.gz'
            seg_path = f'{scan_fldr}/{view.upper()}_seg.nii.gz'
            label_found[view] = False
            try:
                img = nib.load(seg_path)
                imgs[view] = img
                img_found += 1
            except FileNotFoundError:
                imgs[view] = None
                segs[view] = None
                continue
            try:
                segs[view] = nib.load(seg_path)
                seg_found += 1
                label_found[view] = True
            except FileNotFoundError:
                segs[view] = None
                continue
            if imgs[view].shape != segs[view].shape:
                print(f"WARNING: Different shape between {view} image and seg in {scan_fldr}...")
                imgs[view] = None
                segs[view] = None
                continue

        if (seg_found == 0):
            print(f"No segs found in {scan_fldr}. Skipping...")
            continue
        if (img_found != seg_found):
            print(f"WARNING: Different number of images and segs in {scan_fldr}...")

        # Count images
        cont = 0
        for view in views:
            if segs[view] is None: continue
            seg = segs[view].get_fdata()
            frames = np.where(np.sum(seg, axis=(0, 1, 2)) > 0)[0]
            for frame in frames:
                slices = np.where(np.sum(seg[:, :, :, frame], axis=(0, 1)) > 0)[0]
                for slice_idx in slices:
                    cont += 1

        # Create a PDF file to save all the plots
        fig, axes = plt.subplots(int(np.ceil(cont/2)), 2, figsize=(4 * 2, cont // 2 * 4))
        axes = axes.flatten()
        idx = 0
        for view in views:
            if segs[view] is None: continue
            img = imgs[view].get_fdata()
            seg = segs[view].get_fdata()

            frames = np.where(np.sum(seg, axis=(0, 1, 2)) > 0)[0]

            for frame in frames:
                slices = np.where(np.sum(seg[:, :, :, frame], axis=(0, 1)) > 0)[0]

                for slice_idx in slices:
                    ax = axes[idx]

                    # Display the image
                    ax.imshow(img[:, :, slice_idx, frame], cmap='gray', origin='lower')

                    # Overlay the segmentation with transparency
                    segmentation = seg[:, :, slice_idx, frame]

                    masked_seg = np.ma.masked_where(segmentation == 0, segmentation)
                    ax.imshow(masked_seg, cmap='jet_r', alpha=0.4, origin='lower', vmin=1, vmax=3)

                    # Add title and remove axes
                    ax.set_title(f"{scan_fldr}, {view.capitalize()}, Frame {frame}, Slice {slice_idx}")
                    ax.axis('off')

                    idx += 1

        plt.tight_layout()

        # Save the entire figure to the PDF
        pdf.savefig(fig)
        plt.close(fig)
