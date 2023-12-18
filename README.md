# align-atlases-to-bbp

This repository contains scripts used to generate a finite element model of a rat head aligned to the Blue Brain Project Somatosensory cortex model. The workflow is as follows:

The mapping from SIGMA atlas labels to Waxholm atlas labels is created semi-automatically with matchRegions.py. 
The relabelled SIGMA atlas is written using writeRegions.py

The relabelled SIGMA atlas is masked using maskBrain.py

The relabelled SIGMA atlas label field is mapped to the Waxholm atlas using mapSigToWax.sh. The mask from step 2 is used as an input to this step.

The transformation calculated in step 3 is applied to the original SIGMA atlas using transform.sh, which calls transforms.py. This produces an oSPARC rat with the original SIGMA labels.

The mapping from the SIGMA labels to the Paxinos-Watson labels is calculated as in the old pipeline. The output from the previous step is relabelled with the Paxinos-Watson regions using writeRegionsPW.py

The relabelled output from the previous step is aligned to the PW atlas using registerPaxLabelsToFem.sh

The transform calculated in the previos step is applied to the cropped oSPARC rat head label field using transformFullMesh.sh, which calls transformFullMesh.py. This step also applies a scaling of 0.92 in order to match the juvenile rat.
