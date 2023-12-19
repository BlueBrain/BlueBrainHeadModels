# align-atlases-to-bbp

This repository contains scripts used to generate a finite element model of a rat head aligned to the Blue Brain Project Somatosensory cortex model.

## Workflow

The mapping from SIGMA atlas labels to Waxholm atlas labels is created semi-automatically with matchRegions.py. This function loads the lists of tissues for the Waxholm atlas (data/whs_sd_tissuelist.txt) and for the SIGMA atlas (../data/SIGMA_Anatomical_Brain_Atlas_Labels.txt) and creates a mapping between them using fuzzy string matching.

The relabelled SIGMA atlas is written using writeRegions.py. This script loads the original SIGMA atlas (data/SIGMA_Anatomical_Brain_Atlas.nii) and replaces its labels with the Waxholm labels from the previous step.

The relabelled SIGMA atlas is masked using maskBrain.py. This script creates a copy of the relabelled SIGMA atlas, in which only background and non-background are distinguished.

The relabelled SIGMA atlas label field is mapped to the Waxholm atlas using mapSigToWax.sh. This script uses FSL FLIRT to align the relabeld SIGMA atlas to the Waxholm atlas (data/WHS_atlas_prealigned.nii.gz). The mask of the SIGMA atlas, calculated in the previous step, is also used as an input to this step.

The script transform.sh is run next. This first calls the script transform.py, which converts the FSL transformation matrix to an ANTs transformation matrix. transform.sh then applies the ANTs transformation to the original SIGMA atlas. This produces an oSPARC rat with the original SIGMA labels. Note that this step makes use of **data/whs2osparc_bsyn_msb3_Composite.h5**

The mapping from the SIGMA labels to the Paxinos-Watson labels is calculated as in the old pipeline. The output from the previous step is relabelled with the Paxinos-Watson regions using writeRegionsPW.py

The relabelled output from the previous step is aligned to the PW atlas using registerPaxLabelsToFem.sh

The transform calculated in the previos step is applied to the cropped oSPARC rat head label field using transformFullMesh.sh, which calls transformFullMesh.py. This step also applies a scaling of 0.92 in order to match the juvenile rat.
