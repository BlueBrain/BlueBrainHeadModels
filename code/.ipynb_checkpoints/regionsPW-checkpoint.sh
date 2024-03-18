#!/bin/bash
#SBATCH --job-name="EEG"
#SBATCH --partition=prod
#SBATCH --nodes=1
#SBATCH -C cpu
##SBATCH --ntasks-per-node=36
#SBATCH --time=24:00:00
##SBATCH --mail-type=ALL
#SBATCH --output=neurodamus-stdout_new.log
#SBATCH --error=neurodamus-stderr_new.log
#SBATCH --account=proj85
#SBATCH --no-requeue
#SBATCH --exclusive
##SBATCH --qos=bigjob
#ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=6880
export ANTSPATH=~/bin/
export PATH=${ANTSPATH}:$PATH

#~/ANTs/Scripts/antsRegistrationSyNQuick.sh -d 3 -f /gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/osparc_rat_mri.nrrd -m /gpfs/bbp.cscs.ch/project/proj45/scratch/brain_regions.nrrd -t r 

#antsRegistration -o [$thisfolder/pennTemplate_to_${sub}_,$thisfolder/pennTemplate_to_${sub}_Warped.nii.gz] -d 3 -q /gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/osparc_rat_mri.nrrd -r /gpfs/bbp.cscs.ch/project/proj45/scratch/brain_regions.nrrd -t Rigid -m MI --verbose 1 -c [1000x500x250x100,1e-6,10] -f 8x4x2x1 -s 3x2x1x0vox 

#antsApplyTransforms -d 3 -i /gpfs/bbp.cscs.ch/project/proj45/scratch/brain_regions.nrrd -o ADeformed.nii.gz -r /gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/osparc_rat_mri.nrrd -t outputWarped.nii.gz -t output0GenericAffine.mat

#python runAnts.py 
#python writeRegions.py
python writeRegionsPW.py
