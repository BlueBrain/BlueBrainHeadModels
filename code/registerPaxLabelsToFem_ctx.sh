#!/bin/bash
#SBATCH --partition=prod
#SBATCH --nodes=32
#SBATCH -C cpu
#SBATCH --time=24:00:00
#SBATCH --output=paxv2.log
#SBATCH --error=paxerrv2.log
#SBATCH --account=proj85
#SBATCH --no-requeue
#SBATCH --exclusive
##SBATCH --array=0-10

ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=2560

source ../../environments/atlasEnv/bin/activate

export moving_nii='../intermediateFiles/paxLabelsAlignedToOsparcMasked.nii.gz'  # Osparc rat with paxinos-watson labels, with mask applied

export fix_nii='../data/PW_RBSC_6th_indexed_volume.nii.gz' # Paxinos-watson atlas

export in_mask='../intermediateFiles/paxLabelsAlignedToOsparcMask_Ctx.nii.gz' # Mask of osparc rat, from eval.py
export in_mask_binary='../intermediateFiles/paxLabelsAlignedToOsparcMask.nii.gz' # Mask of osparc rat, from eval.py

export ref_mask='../intermediateFiles/PWMaskMask_Ctx.nii.gz' # Mask of paxinos-watson atlas, from eval.py
export ref_mask_binary='../intermediateFiles/PWMaskBinary.nii.gz' # Mask of paxinos-watson atlas, from eval.py

export transform_osparc_to_pw='../intermediateFiles/pwMatrix.mat' # FSL transformation matrix that aligns osparc rat to paxinos-watson atlas
export transform_osparc_to_pw_final='../intermediateFiles/pwMatrix_Ctx.mat' # FSL transformation matrix that aligns osparc rat to paxinos-watson atlas

export unused_output_image='../intermediateFiles/pwOutput.nii.gz'

python eval_cortex.py #$SLURM_ARRAY_TASK_ID

wait

#echo "Done with eval"


flirt -paddingsize 400 -refweight $ref_mask -inweight $in_mask -searchcost labeldiff -interp nearestneighbour -datatype int -cost labeldiff -omat $transform_osparc_to_pw_final -searchrx -180 180 -searchry -180 180 -searchrz -180 180 -v -in $moving_nii -ref $fix_nii -out $unused_output_image
