#!/bin/bash  
#SBATCH --job-name="EEG"
#SBATCH --partition=prod
#SBATCH --nodes=1
#SBATCH -C cpu
#SBATCH --time=24:00:00 
#SBATCH --account=proj85

export moving_nii='/gpfs/bbp.cscs.ch/project/proj45/scratch/newRegistration/sig_with_paxRegions.nii.gz'
export fix_nii='/gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/WHS_atlas_prealigned.nii.gz' 
export moving_mask='/gpfs/bbp.cscs.ch/project/proj45/scratch/newRegistration/mask.nii.gz'

flirt -inweight $moving_mask -paddingsize 400 -searchcost labeldiff -interp nearestneighbour -datatype int -cost labeldiff -omat matrix.mat -searchrx -180 180 -searchry -180 180 -searchrz -180 180 -v -in $moving_nii -ref $fix_nii -out output.nii.gz 
