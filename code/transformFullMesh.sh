#!/bin/bash
#SBATCH --job-name="EEG"
#SBATCH --partition=prod
#SBATCH --nodes=1
#SBATCH -C cpu
##SBATCH --ntasks-per-node=36
#SBATCH --time=24:00:00
#SBATCH --account=proj85
#SBATCH --no-requeue
#SBATCH --exclusive
#SBATCH --mem=0


ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=9000
export ANTSPATH=~/bin/
export PATH=${ANTSPATH}:$PATH
export fix_label='../data/PW_RBSC_6th_indexed_volume_pad_full.nii.gz'
export moving_nii='../data/20200810_segmentation_cropped.nii.gz'

python transformFullMesh.py

antsApplyTransforms --dimensionality 3 \
                    --input ${moving_nii} \
		    --reference-image ${fix_label}\
                    --transform [transformFullMesh.mat, 0] \
                    --output garbageFull.nii.gz \
                    --interpolation NearestNeighbor\
			-v 1

 
