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
export fix_label='../data/WHS_atlas_prealigned_pad.nii.gz'
export moving_nii='../data/SIGMA_Anatomical_Brain_Atlas.nii'
export final_ref='../intermediateFiles/whs2osparc_bsyn_msb3_whs_atlas_aligned_osparcratwears.nii.gz'

python transforms.py

antsApplyTransforms --dimensionality 3 \
                    --input ${moving_nii} \
                    --reference-image ${fix_label} \
                    --transform [transform.mat, 0] \
                    --output outputSigLabels.nii.gz \
                    --interpolation NearestNeighbor

antsApplyTransforms --dimensionality 3\
		    --input outputSigLabels.nii.gz\
		    --transform whs2osparc_bsyn_msb3_Composite.h5\
                    --reference-image ${final_ref}\
		    --output sigLabelsAlignedToOsparc.nii.gz\
		    --interpolation NearestNeighbor 
