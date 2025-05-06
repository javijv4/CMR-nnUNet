#!/bin/bash
id=$1
mode=$2

# Train all the folds 
for i in {0..5}
do
    echo $id $mode $i
    nnUNetv2_train $id $mode $i --npz
done