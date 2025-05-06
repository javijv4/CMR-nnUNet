#!/bin/bash
# LA is trained with 2d 
mode=2d
for id in 42 43 44      # 2CH 3CH 4CH
do
    # Train all the folds 
    for i in {0..5}
    do
        echo $id $mode $i
        nnUNetv2_train $id $mode $i --npz
        nnUNetv2_find_best_configuration $id -c $mode
    done
done

# SA is trained with 2d and 3d_fullres
id=41

mode=2d
# Train all the folds 
for i in {0..5}
do
    echo $id $mode $i
    nnUNetv2_train $id $mode $i --npz
    nnUNetv2_find_best_configuration $id -c $mode
done


mode=3d_fullres
# Train all the folds 
for i in {0..5}
do
    echo $id $mode $i
    nnUNetv2_train $id $mode $i --npz
    nnUNetv2_find_best_configuration $id -c $mode
done
