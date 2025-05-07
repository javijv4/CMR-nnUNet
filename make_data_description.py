#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
Created on 2025/04/02 09:12:58

@author: Javiera Jilberto Vallejos 
'''

import nibabel as nib

from tqdm import tqdm
import csv

from glob import glob

views = ['sa', '2ch', '3ch', '4ch']

folders = glob('nn_data/scan*')
folders = sorted(folders, key=lambda x: int(x[-3:]))

#%%
data = []
for scan_fldr in tqdm(folders):
    i = int(scan_fldr[-3:])

    f = open(f'{scan_fldr}/info.txt', 'r')
    lines = f.readlines()
    f.close()

    string = [scan_fldr, lines[0].strip()]

    label_found = {}
    for view in views:
        seg_path = f'{scan_fldr}/{view.upper()}_seg.nii.gz'
        try:
            seg = nib.load(seg_path)
            label_found[view] = True
        except FileNotFoundError:
            label_found[view] = False
            seg = None

    for key in label_found.keys():
        if label_found[key]:
            string.append("yes")
        else:
            string.append("")
 
    data.append(string)

#%%
# Save data to a CSV file
with open('nn_data/data_description.csv', mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Scan Folder', 'Info'])  # Write header
    writer.writerows(data)  # Write data rows
    