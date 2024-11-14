#!/bin/bash
path=test_data
mode=2d
id=42
name=2CH

# Inference
python3 split_nii.py $path/ $name
nnUNetv2_predict -i $path/imgs/ -o $path/segs/ -d $id -c $mode 
python3 join_nii.py $path/ $name

# Cleaning
rm -r $path/imgs
rm -r $path/segs