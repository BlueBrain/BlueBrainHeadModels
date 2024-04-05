#!/bin/bash
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
source path_to_pip_env # Needs to be set by the user

export ANTSPATH='path_to_ants_installation' # Needs to be set by the user

export PATH=${ANTSPATH}:$PATH

export fix_label='../intermediateFiles/Paxinos_Watson_Atlas_padded.nii.gz' # Paxinos watson atlas, resized to match cropped osparc rat head. Produced by convert_to_ants_transform_neurorat_to_paxinos_watson.py

export moving_nii='../data/Neurorat.nii.gz'  # Cropped NeuroRat head

export transform='../intermediateFiles/transformNeuroratToPaxinosWatson_ANTs.mat' # ANTs transformation matrix to align NeuroRat to paxinos-watson atlas. Produced by convert_to_ants_transform_neurorat_to_paxinos_watson.py

export output='alignedModel.nii.gz'
 

python convert_to_ants_transform_neurorat_to_paxinos_watson.py

antsApplyTransforms --dimensionality 3 \
                    --input ${moving_nii} \
                    --reference-image ${fix_label}\
                   --transform [${transform}, 0] \
                   --output ${output} \
                    --interpolation NearestNeighbor\
                    -v 1


