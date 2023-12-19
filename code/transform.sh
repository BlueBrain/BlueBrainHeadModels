#!/bin/bash
#SBATCH --job-name="EEG"
#SBATCH --partition=prod
#SBATCH --nodes=16
#SBATCH -C nvme|cpu
##SBATCH --ntasks-per-node=36
#SBATCH --time=24:00:00
##SBATCH --mail-type=ALL
#SBATCH --output=neurodamus-stdout_new.log
#SBATCH --error=neurodamus-stderr_new.log
#SBATCH --account=proj85
#SBATCH --no-requeue
#SBATCH --exclusive
#SBATCH --mem=0
##SBATCH --qos=bigjob

#ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=6880
export ANTSPATH=~/bin/
export PATH=${ANTSPATH}:$PATH

export fix_label='../data/WHS_atlas_prealigned.nii.gz' # Waxholm atlas

export moving_nii='../data/SIGMA_Anatomical_Brain_Atlas.nii' # SIGMA atlas

export sigma_to_wax='../intermediateFiles/sigmaToWax.nii.gz' #SIGMA atlas aligned to Waxholm atlas

export final_ref='../data/whs2osparc_bsyn_msb3_whs_atlas_aligned_osparcratwears.nii.gz' # Waxholm atlas aligned to oSPARC rat

export final_transform='../data/whs2osparc_bsyn_msb3_Composite.h5' # Transform aligning waxholm atlas to oSPARC rat

export sigma_to_osparc='../intermediateData/sigLabelsAlignedToOsparc.nii.gz'

python transforms.py

## First step aligns sigma atlas to waxholm atlas

antsApplyTransforms --dimensionality 3 \
                    --input ${moving_nii} \
                    --reference-image ${fix_label} \
                    --transform [transform.mat, 0] \
                    --output $sigma_to_wax \
                    --interpolation NearestNeighbor

# Second step aligns sigma atlas to oSPARC Rat

antsApplyTransforms --dimensionality 3\
		    --input $sigma_to_wax\
		    --transform $final_transform\
                    --reference-image ${final_ref}\
		    --output $sigma_to_osparc\
		    --interpolation NearestNeighbor 
