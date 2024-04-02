#!/bin/bash  
#SBATCH --partition=prod
#SBATCH --nodes=1
#SBATCH -C cpu
#SBATCH --time=24:00:00 
#SBATCH --account=proj85
#SBATCH --mem=0

export moving_nii='../intermediateFiles/sig_with_waxRegions.nii.gz' # Sigma atlas with waxholm labels, produced by writeRegions.py
export fix_nii='../data/WHS_atlas_prealigned.nii.gz' # Waxholm atlas
export moving_mask='../intermediateFiles/mask.nii.gz' # Mask of SIGMA atlas, produced by maskBrain.py

export output_transformation_matrix='../intermediateFiles/matrixSigmaToWaxholm_FSL.mat' # Transformation matrix
export output_image='../intermediateFiles/outputSigmaToWaxholm.nii.gz' # Unused output image

flirt -inweight $moving_mask -paddingsize 400 -searchcost labeldiff -interp nearestneighbour -datatype int -cost labeldiff -omat $output_transformation_matrix -searchrx -180 180 -searchry -180 180 -searchrz -180 180 -v -in $moving_nii -ref $fix_nii -out $output_image 
