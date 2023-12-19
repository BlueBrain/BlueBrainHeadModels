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

export fix_label='../data/PW_RBSC_6th_indexed_volume_pad_full.nii.gz' # Paxinos watson atlas, resized to match cropped osparc rat head. Produced by transformFullMesh.py

export moving_nii='../data/20200810_segmentation_cropped.nii.gz' # Cropped osparc rat head

export transform='../intermediateData/transformFullMesh.mat' # ANTs transformation matrix to align osparc to paxinos-watson atlas. Produced by transformFullMesh.py

export output='alignedModel.nii.gz'

python transformFullMesh.py

antsApplyTransforms --dimensionality 3 \
                    --input ${moving_nii} \
		    --reference-image ${fix_label}\
                    --transform [$transform, 0] \
                    --output $final_output \
                    --interpolation NearestNeighbor\
			-v 1

 
