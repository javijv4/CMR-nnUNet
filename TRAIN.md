## Instructions for training the NN in a certain dataset
For everything below, change the DATASET_NAME, DATASET_ID, and CONFIGURATION, to any of the following
* SA, 41, 3d_fullres
* LA_2CH, 42, 2d
* LA_3CH, 43, 2d
* LA_4CH, 44, 2d

Prepare dataset 
```
python -m makeNN_dataset.py -i datasets/DATASET_NAME -t DATASET_NAME -d DATASET_ID
nnUNetv2_plan_and_preprocess -d DATASET_ID --verify_dataset_integrity
```
Train the NN
```
bash train.sh DATASET_ID
nnUNetv2_find_best_configuration DATASET_ID -c CONFIGURATION
```
Export to a zip file
```
nnUNetv2_export_model_to_zip -d DATASET_ID -c CONFIGURATION -o models/nn_DATASET_NAME.zip
```
