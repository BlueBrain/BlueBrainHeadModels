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

export moving_nii='/gpfs/bbp.cscs.ch/project/proj45/scratch/newRegistration/paxLabelsAlignedToOsparcMasked.nii.gz'
export fix_nii='/gpfs/bbp.cscs.ch/project/proj68/home/bolanos/Paxinos/raw/NII/PW_RBSC_6th_indexed_volume.nii.gz'
export in_mask='/gpfs/bbp.cscs.ch/project/proj45/scratch/newRegistration/paxLabelsAlignedToOsparcMask.nii.gz'
export ref_mask='/gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/PWMaskMask.nii.gz'

flirt -paddingsize 400 -refweight $ref_mask -inweight $in_mask -searchcost labeldiff -interp nearestneighbour -datatype int -cost labeldiff -omat pwMatrix.mat -searchrx -180 180 -searchry -180 180 -searchrz -180 180 -v -in $moving_nii -ref $fix_nii -out pwOutput.nii.gz

#flirt -in $fix_nii -out output.nii.gz -ref $moving_nii -applyxfm -init matrix
#tration --dimensionality 3 --float 0 --interpolation BSpline \
#                 --use-histogram-matching 1 \
#                 --winsorize-image-intensities [0.005,0.995] \
#                 --output [${OUTPUT_PREFIX},${OUTPUT_PREFIX}Warped.nii.gz,${OUTPUT_PREFIX}InverseWarped.nii.gz] \
#                 --initial-moving-transform [${fix_nii},${moving_nii},1] \
 #                --transform translation[0.1] \
 #                  --metric MI[${fix_nii},${moving_nii},1,32,Random,0.25] \
 #                  --convergence [50,1e-6,10] \
 #                  --shrink-factors 1 \
 #                  --smoothing-sigmas 0vox \
 #                --transform Rigid[0.05] \
 #                  --metric MI[${fix_nii},${moving_nii},1,64,Random,0.25] \
 #                  --convergence [500x250x50,1e-6,10] \
 #                  --shrink-factors 2x2x1 \
 #                  --smoothing-sigmas 2x1x0vox \
 #                --transform SyN[0.1,3,0] \
 #                  --metric CC[${fix_nii},${moving_nii},1,4] \
 #                  --convergence [50x10,1e-6,10] \
 #                  --shrink-factors 2x1 \
 #                  --smoothing-sigmas 1x0vox \

#antsApplyTransforms --dimensionality 3 \
#                    --input ${fix_nii} \
  #                  --reference-image ${moving_nii} \
 #                   --transform [pax0GenericAffine.mat, 1] \
  #                  --transform pax1InverseWarp.nii.gz \
 #                   --output paxlabel2epi0pad.nii.gz \
 #                   --interpolation NearestNeighbor
#~/ANTs/Scripts/antsRegistrationSyNQuick.sh -d 3 -f /gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/osparc_rat_mri.nrrd -m /gpfs/bbp.cscs.ch/project/proj45/scratch/brain_regions.nrrd -t r 

#antsRegistration -o [$thisfolder/pennTemplate_to_${sub}_,$thisfolder/pennTemplate_to_${sub}_Warped.nii.gz] -d 3 -q /gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/osparc_rat_mri.nrrd -r /gpfs/bbp.cscs.ch/project/proj45/scratch/brain_regions.nrrd -t Rigid -m MI --verbose 1 -c [1000x500x250x100,1e-6,10] -f 8x4x2x1 -s 3x2x1x0vox 

#antsApplyTransforms -d 3 -i /gpfs/bbp.cscs.ch/project/proj45/scratch/brain_regions.nrrd -o ADeformed.nii.gz -r /gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/osparc_rat_mri.nrrd -t outputWarped.nii.gz -t output0GenericAffine.mat

#python runAnts.py 
#python registration.py
