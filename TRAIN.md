## Instructions for training the NN in a certain dataset
For everything below, change the DATASET_NAME, DATASET_ID, and CONFIGURATION, to any of the following
* SA, 41, 2d or 3d_fullres
* LA_2CH, 42, 2d
* LA_3CH, 43, 2d
* LA_4CH, 44, 2d

1. Create training and testing datasets: run `create_training_and_testing.py` for the views of interests.
2. (not sure if this is totally needed, but it seems you need to delete the dataset folders in the NN path)
2. Prepare dataset 
```
python makeNN_dataset.py -i datasets/DATASET_NAME -t DATASET_NAME -d DATASET_ID
nnUNetv2_plan_and_preprocess -d DATASET_ID --verify_dataset_integrity
```
3. Train the NN. `fold` is an integer from 0 to 4. You need to repeat this for 5 folds.
```
nnUNetv2_train DATASET_ID CONFIGURATION fold --npz
```
4. Find the best configuration considering all the folds
```
nnUNetv2_find_best_configuration DATASET_ID -c CONFIGURATION
5. Export to a zip file
```
nnUNetv2_export_model_to_zip -d DATASET_ID -c CONFIGURATION -o models/nn_DATASET_NAME.zip
```

Steps 3 and 4 for all views can be run automatically using `train_all.sh`.