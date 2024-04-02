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
source ../../environments/atlasEnv/bin/activate  # Needs to be set by the user

export ANTSPATH='/gpfs/bbp.cscs.ch/project/proj85/bin/' # Needs to be set by the user

export PATH=${ANTSPATH}:$PATH

export fix_label='../intermediateFiles/PW_RBSC_6th_indexed_volume_pad_full.nii.gz' # Paxinos watson atlas, resized to match cropped osparc rat head. Produced by transformFullMeshBig.py

export moving_nii='../data/Crop-20210802.nii.gz'  # Cropped osparc rat head

export final_ref='../data/whs2osparc_bsyn_msb3_whs_atlas_aligned_osparcratwears.nii.gz' 

export transform='../intermediateFiles/transformFullMesh_ctx.mat' # ANTs transformation matrix to align osparc to paxinos-watson atlas. Produced by transformFullMesh.py

export output='alignedModel_ctx.nii.gz'
 

python transformFullMeshBig_cortex.py $SLURM_ARRAY_TASK_ID

wait

antsApplyTransforms --dimensionality 3 \
                    --input ${moving_nii} \
                    --reference-image ${fix_label}\
                   --transform [${transform}, 0] \
                   --output ${output} \
                    --interpolation NearestNeighbor\
                    -v 1


