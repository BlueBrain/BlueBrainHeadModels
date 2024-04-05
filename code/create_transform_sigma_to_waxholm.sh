#!/bin/bash  
#SBATCH --partition=prod
#SBATCH --nodes=1
#SBATCH -C cpu
#SBATCH --time=24:00:00 
#SBATCH --account=proj85
#SBATCH --mem=0

export moving_nii='../intermediateFiles/sigma_atlas_with_waxholm_labels.nii.gz' # Sigma atlas with waxholm labels, produced by write_waxholm_regions_to_sigma_atlas.py

export fix_nii='../data/Waxholm_Atlas.nii.gz' # Waxholm atlas

export moving_mask='../intermediateFiles/mask_of_sigma_atlas.nii.gz' # Mask of SIGMA atlas, produced by mask_sigma_atlas.py

export output_transformation_matrix='../intermediateFiles/matrixSigmaToWaxholm_FSL.mat' # Transformation matrix

export output_image='../intermediateFiles/outputSigmaToWaxholm.nii.gz' # Unused output image

flirt -inweight $moving_mask -paddingsize 400 -searchcost labeldiff -interp nearestneighbour -datatype int -cost labeldiff -omat $output_transformation_matrix -searchrx -180 180 -searchry -180 180 -searchrz -180 180 -v -in $moving_nii -ref $fix_nii -out $output_image 
