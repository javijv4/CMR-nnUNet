#!/bin/bash
# SA is trained with 2d and 3d_fullres
id=41
mode=2d

# Train all the folds 
for i in {0..5}
do
    echo $id $mode $i
    nnUNetv2_train $id $mode $i --npz
done
nnUNetv2_find_best_configuration $id -c $mode


mode=3d_fullres
# Train all the folds 
for i in {0..5}
do
    echo $id $mode $i
    nnUNetv2_train $id $mode $i --npz
done
nnUNetv2_find_best_configuration $id -c $mode
