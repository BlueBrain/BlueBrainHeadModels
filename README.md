# align-atlases-to-bbp

This repository contains scripts used to generate a finite element model of a rat head aligned to the Blue Brain Project Somatosensory cortex model.

## Dependencies and configuration instructions

This pieline depends on ANTs Version: 2.3.4.dev206-g2251c, and on fsl flirt version 6.0, both of which must be installed by the user. The user must ensure that FSL is available from the command line (e.g., by modifying their ~/.bash_profile file) for this pipeline to work. 

This pipeline also depends on the python packages listed in the requirements.txt file, which can be pip installed. 

You will have to update the paths in the bash scripts to your ANTs installation and to the location of your pip virtual environment. When running python scripts from the terminal, please ensure you have your virtual environment active

This pipeline was run on a CentOS Linux cluster with the slurm job submission system; the bash scripts assume that this is true of your system as well. 

## Workflow

1. The mapping from SIGMA atlas labels to Waxholm atlas labels is created semi-automatically with matchRegions.py (run from the terminal). This function loads the lists of tissues for the Waxholm atlas (data/whs_sd_tissuelist.txt) and for the SIGMA atlas (../data/SIGMA_Anatomical_Brain_Atlas_Labels.txt) and creates a mapping between them using fuzzy string matching. For each pair, the user must either accept the match, by entering the return key, or provide an alternative region name.

2. The relabelled SIGMA atlas is written using writeRegions.py (run from the terminal). This script loads the original SIGMA atlas (data/SIGMA_Anatomical_Brain_Atlas.nii) and replaces its labels with the Waxholm labels from the previous step.

3. The relabelled SIGMA atlas is masked using maskBrain.py (run from the terminal). This script creates a copy of the relabelled SIGMA atlas, in which only background and non-background are distinguished.

4. The relabelled SIGMA atlas label field is mapped to the Waxholm atlas using mapSigToWax.sh. This script uses FSL FLIRT to align the relabeld SIGMA atlas to the Waxholm atlas (data/WHS_atlas_prealigned.nii.gz). The mask of the SIGMA atlas, calculated in the previous step, is also used as an input to this step.

5. The script transform.sh is run next. This first calls the script transform.py, which converts the FSL transformation matrix to an ANTs transformation matrix. transform.sh then applies the ANTs transformation to the original SIGMA atlas; this produces a Waxholm rat with the original SIGMA labels.  This step then makes use the transform defined in data/whs2osparc_bsyn_msb3_Composite.h5, which aligns the waxholm rat with the oSPARC rat, to align the SIGMA-labeled waxholm rat to the oSPARC rat, thus producing an oSPARC rat with SIGMA labels.

6. The mapping from the SIGMA labels to the Paxinos-Watson labels is calculated using the script **matchRegions_SigmaToPW.py** (run from the terminal). This loads the lists of tissues for the Paxinos-Watson atlas (data/PW_RBSC_6th_cortex.txt for the cortex and data/PW_RBSC_6th_lut.txt for the whole brain) and creates a mapping between them and the list of tissues in the SIGMA atlas using fuzzy string matching.

7. The oSPARC rat with SIGMA labels is then relabelled with the Paxinos-Watson regions using writeRegionsPW.py (run from the terminal)

8. Next, the script eval.py is run from the terminal. This script creates a mask of the osparc rat, and of the paxinos-watson atlas.

9. The masked image created in step 8 is aligned to the PW atlas using registerPaxLabelsToFem.sh This script loads the Paxinos Watson atlas (data/PW_RBSC_6th_indexed_volume.nii.gz), the oSparc rat with paxinos-watson labels, and the masks for each of these two atlases, and uses FSL FLIRT to align the oSparc rat to the PW atlas.

10. The transform calculated in the previous step is applied to the cropped oSPARC rat head label field using transformFullMeshBig.sh. This script first calls transformFullMeshBig.py, which loads the FSL transformation matrix that maps the osparc rat to the Paxinos-Watson atlas, and writes it as an ANTs transform. The script then resizes the paxions-watson atlas to match the size of the cropped osparc rat head (data/Crop-20210802.nii.gz) plus 100 pixels of padding. The script transformFullMeshBig.sh then loads the oSparc  rat head (data/Crop-20210802.nii.gz),  the padded Paxinos-Watson image, and aligns the former to the latter using the ANTs transform generated by transformFullMeshBig.py. This step also applies a scaling of 0.92 in order to match the juvenile rat.

## Citation
If you use this software, we kindly ask you to cite the following publication: BlueRecording: A Pipeline for efficient calculation of extracellular recordings in large-scale neural circuit models

## Acknowledgment
The development of this software was supported by funding to the Blue Brain Project, a research center of the École polytechnique fédérale de Lausanne (EPFL), from the Swiss government's ETH Board of the Swiss Federal Institutes of Technology.

Copyright (c) 2023 Blue Brain Project/EPFL
