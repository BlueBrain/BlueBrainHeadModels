#!/bin/bash
#SBATCH --partition=prod
#SBATCH --nodes=16
#SBATCH -C cpu
##SBATCH --ntasks-per-node=36
#SBATCH --time=24:00:00
#SBATCH --account=proj85
#SBATCH --no-requeue
#SBATCH --exclusive
#SBATCH --mem=0


source path_to_pip_env # Needs to be set by the user

export ANTSPATH='path_to_ants_installation' # Needs to be set by the user
export PATH=${ANTSPATH}:$PATH

export fix_label='../data/Waxholm_Atlas.nii.gz' # Waxholm atlas

export moving_nii='../data/SIGMA_Anatomical_Brain_Atlas.nii' # SIGMA atlas

export sigma_to_wax='../intermediateFiles/sigma_atlas_transformed_to_waxholm_space.nii.gz' #SIGMA atlas aligned to Waxholm atlas - output of this stage

export final_ref='../data/waxholm_aligned_to_neurorat.nii.gz' # Waxholm atlas aligned to NeuroRat

export final_transform='../data/transform_waxholm_to_neurorat.h5' # Transform aligning waxholm atlas to NeuroRat

export sigma_to_neurorat='../intermediateFiles/sigma_atlas_transfomed_to_neurorat_space.nii.gz'

export antsTransform='../intermediateFiles/transformSigmaToWaxholm_ANTS.mat'

python convert_to_ants_transform_sigma_to_waxholm.py

## First step aligns sigma atlas to waxholm atlas

antsApplyTransforms --dimensionality 3 \
                    --input ${moving_nii} \
                    --reference-image ${fix_label} \
                    --transform [$antsTransform, 0] \
                    --output $sigma_to_wax \
                    --interpolation NearestNeighbor

# Second step aligns sigma atlas to oSPARC Rat

antsApplyTransforms --dimensionality 3\
		    --input $sigma_to_wax\
		    --transform $final_transform\
                    --reference-image ${final_ref}\
		    --output $sigma_to_neurorat\
		    --interpolation NearestNeighbor 
