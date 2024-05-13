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
# SPDX-License-Identifier: Apache-2.0

ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=2560


export moving_nii='../intermediateFiles/neurorat_with_paxinos_watson_labels_masked.nii.gz'  # NeuroRat with paxinos-watson labels, with mask applied. From mask_neurorat_and_paxinos_watson.py

export fix_nii='../data/Paxinos_Watson_Atlas.nii.gz' # Paxinos-watson atlas

export in_mask='../intermediateFiles/neurorat_with_paxinos_watson_labels_mask.nii.gz' # Mask of NeuroRat, from mask_neurorat_and_paxinos_watson.py

export ref_mask='../intermediateFiles/Paxinos_Watson_Atlas_Mask.nii.gz' # Mask of paxinos-watson atlas, from mask_neurorat_and_paxinos_watson.py

export transform_osparc_to_pw='../intermediateFiles/matrixNeuroratToPaxinosWatson_FSL.mat' # FSL transformation matrix that aligns NeuroRat to paxinos-watson atlas

export unused_output_image='../intermediateFiles/pwOutput.nii.gz'

flirt -paddingsize 400 -refweight $ref_mask -inweight $in_mask -searchcost labeldiff -interp nearestneighbour -datatype int -cost labeldiff -omat $transform_osparc_to_pw -searchrx -180 180 -searchry -180 180 -searchrz -180 180 -v -in $moving_nii -ref $fix_nii -out $unused_output_image

