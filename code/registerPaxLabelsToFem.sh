#!/bin/bash
#SBATCH --partition=prod
#SBATCH --nodes=32
#SBATCH -C cpu
#SBATCH --time=24:00:00
#SBATCH --output=pax.log
#SBATCH --error=paxerr.log
#SBATCH --account=proj85
#SBATCH --no-requeue
#SBATCH --exclusive

ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=2560

export ANTSPATH='path_to_ants_installation' # Needs to be set by the user
export PATH=${ANTSPATH}:$PATH

export moving_nii='../intermediateFiles/paxLabelsAlignedToOsparcMasked.nii.gz'  # Osparc rat with paxinos-watson labels, with mask applied

export fix_nii='../data/PW_RBSC_6th_indexed_volume.nii.gz' # Paxinos-watson atlas

export in_mask='../intermediateFiles/paxLabelsAlignedToOsparcMask.nii.gz' # Mask of osparc rat, from eval.py

export ref_mask='../intermediateFiles/PWMaskMask.nii.gz' # Mask of paxinos-watson atlas, from eval.py

export transform_osparc_to_pw='../intermediateFiles/pwMatrix.mat' # FSL transformation matrix that aligns osparc rat to paxinos-watson atlas

export unused_output_image='../intermediateFiles/pwOutput.nii.gz'

flirt -paddingsize 400 -refweight $ref_mask -inweight $in_mask -searchcost labeldiff -interp nearestneighbour -datatype int -cost labeldiff -omat $transform_osparc_to_pw -searchrx -180 180 -searchry -180 180 -searchrz -180 180 -v -in $moving_nii -ref $fix_nii -out $unused_output_image

