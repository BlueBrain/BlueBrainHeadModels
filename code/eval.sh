#!/bin/bash
#SBATCH --job-name="EEG"
#SBATCH --partition=prod
#SBATCH --nodes=1
#SBATCH -C cpu
##SBATCH --ntasks-per-node=36
#SBATCH --time=24:00:00
##SBATCH --mail-type=ALL
#SBATCH --output=eval.log
#SBATCH --error=evalerr.log
#SBATCH --account=proj85
#SBATCH --no-requeue
#SBATCH --exclusive
##SBATCH --qos=bigjob

#ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=6880
export ANTSPATH=~/bin/
export PATH=${ANTSPATH}:$PATH

python eval.py
