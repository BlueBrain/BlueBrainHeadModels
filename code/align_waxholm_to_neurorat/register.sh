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
# SPDX-License-Identifier: Apache-2.0


source ../../../environments/atlasEnv/bin/activate # Needs to be set by the user


python register_waxholm2aic.py 

