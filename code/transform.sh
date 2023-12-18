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
export fix_label='/gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/WHS_atlas_prealigned_pad.nii.gz'
export moving_nii='/gpfs/bbp.cscs.ch/project/proj45/scratch/SIGMA_Wistar_Rat_Brain_TemplatesAndAtlases_Version1.1/SIGMA_Rat_Brain_Atlases/SIGMA_Anatomical_Atlas/SIGMA_Anatomical_Brain_Atlas.nii'
export final_ref='/gpfs/bbp.cscs.ch/project/proj45/scratch/newRegistration/whs2osparc_bsyn_msb3_whs_atlas_aligned_osparcratwears.nii.gz'
#~/ANTs/Scripts/antsRegistrationSyNQuick.sh -d 3 -f /gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/osparc_rat_mri.nrrd -m /gpfs/bbp.cscs.ch/project/proj45/scratch/brain_regions.nrrd -t r 

#antsRegistration -o [$thisfolder/pennTemplate_to_${sub}_,$thisfolder/pennTemplate_to_${sub}_Warped.nii.gz] -d 3 -q /gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/osparc_rat_mri.nrrd -r /gpfs/bbp.cscs.ch/project/proj45/scratch/brain_regions.nrrd -t Rigid -m MI --verbose 1 -c [1000x500x250x100,1e-6,10] -f 8x4x2x1 -s 3x2x1x0vox 

#antsApplyTransforms -d 3 -i /gpfs/bbp.cscs.ch/project/proj45/scratch/brain_regions.nrrd -o ADeformed.nii.gz -r /gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/osparc_rat_mri.nrrd -t outputWarped.nii.gz -t output0GenericAffine.mat

#python runAnts.py 
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
