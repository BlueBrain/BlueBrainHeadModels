#!/bin/bash
#SBATCH --job-name="EEG"
#SBATCH --partition=prod
#SBATCH --nodes=32
#SBATCH -C nvme|cpu
##SBATCH --ntasks-per-node=36
#SBATCH --time=24:00:00
##SBATCH --mail-type=ALL
#SBATCH --output=pax.log
#SBATCH --error=paxerr.log
#SBATCH --account=proj85
#SBATCH --no-requeue
#SBATCH --exclusive
#SBATCH --qos=bigjob

ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=2560

export ANTSPATH=~/bin/
export PATH=${ANTSPATH}:$PATH
export OUTPUT_PREFIX='pax'

export moving_nii='../intermediateData/paxLabelsAlignedToOsparcMasked.nii.gz' 

export fix_nii='../data/PW_RBSC_6th_indexed_volume.nii.gz' # Paxinos-watson atlas

export in_mask='../intermediateData/paxLabelsAlignedToOsparcMask.nii.gz'

export ref_mask='../intermediateData/PWMaskMask.nii.gz'

export transform_osparc_to_pw='../intermediateData/pwMatrix.mat' # FSL transformation matrix that aligns osparc rat to paxinos-watson atlas

export unused_output_image='..intermediateData/pwOutput.nii.gz'

flirt -paddingsize 400 -refweight $ref_mask -inweight $in_mask -searchcost labeldiff -interp nearestneighbour -datatype int -cost labeldiff -omat $transform_osparc_to_pw -searchrx -180 180 -searchry -180 180 -searchrz -180 180 -v -in $moving_nii -ref $fix_nii -out $unused_output_image

