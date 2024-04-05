# BlueBrainHeadModels

This repository contains scripts used to generate a finite element model of a rat head aligned to the Blue Brain Project Somatosensory cortex model.

## Dependencies and configuration instructions

This pipeline depends on ANTs Version: 2.3.4.dev206-g2251c, and on fsl flirt version 6.0, both of which must be installed by the user. The user must ensure that FSL is available from the command line (e.g., by modifying their ~/.bash_profile file) for this pipeline to work. 

This pipeline also depends on the python packages listed in the requirements.txt file, which can be pip installed. 

You will have to update the paths in the bash scripts to your ANTs installation and to the location of your pip virtual environment. When running python scripts from the terminal, please ensure you have your virtual environment active

This pipeline was run on a CentOS Linux cluster with the slurm job submission system; the bash scripts assume that this is true of your system as well. 

## Input data

This pipeline aligns the  ViZOO NeuroRat (150g) model V4.0 (DOI: 10.13099/VIP91106-04-1, https://itis.swiss/virtual-population/animal-models/animals/neurorat/) to the Paxinos Watson atlas. In intermediate steps, it uses the SIGMA atlas (https://www.nitrc.org/projects/sigma_template) and the Waxholm Atlas (https://www.nitrc.org/projects/whs-sd-atlas). 

All input data can be downloaded from 10.5281/zenodo.10926947 and should be saved to the *data* folder before beginning the workflow.

## Workflow

1. A mapping from SIGMA atlas labels to Waxholm atlas labels is created semi-automatically with match_waxholm_regions_to_sigma_atlas.py (run from the terminal). This function loads the lists of tissues for the Waxholm atlas (data/Waxholm_Atlas_Labels.txt) and for the SIGMA atlas (../data/SIGMA_Anatomical_Brain_Atlas_Labels.txt) and creates a mapping between them using fuzzy string matching. For each pair, the user must either accept the match, by entering the return key, or provide an alternative region name.

2. A relabelled SIGMA atlas is written using write_waxholm_regions_to_sigma_atlas.py (run from the terminal). This script loads the original SIGMA atlas (data/SIGMA_Anatomical_Brain_Atlas.nii) and replaces its labels with the Waxholm labels from the previous step.

3. The relabelled SIGMA atlas is masked using mask_sigma_atlas.py (run from the terminal). This script creates a copy of the relabelled SIGMA atlas, in which only background and non-background are distinguished.

4. The relabelled SIGMA atlas label field is mapped to the Waxholm atlas using create_transform_sigma_to_waxholm.sh. This script uses FSL FLIRT to align the relabeled SIGMA atlas to the Waxholm atlas (data/Waxholm_Atlas.nii.gz). The mask of the SIGMA atlas, calculated in the previous step, is also used as an input to this step.

5. The script transform_sigma_atlas_to_neurorat_space.sh is run next. This first calls the script convert_to_ants_transform_sigma_to_waxholm.py, which converts the FSL transformation matrix from the previous step to an ANTs transformation matrix.

transform_sigma_atlas_to_neurorat_space.sh then applies the ANTs transformation to the original SIGMA atlas; this produces a Waxholm rat with the original SIGMA labels. 

It then makes use the transform defined in data/transform_waxholm_to_neurorat.h5, which aligns the Waxholm rat with the Neurorat, to align the SIGMA-labeled Waxholm rat to the Neurorat, thus producing a Neurorat with SIGMA labels.

6. The mapping from the SIGMA labels to the Paxinos-Watson labels is calculated using the script **match_sigma_regions_to_paxinos_watson_atlas.py** (run from the terminal). This loads the lists of tissues for the Paxinos Watson atlas (data/Paxinos_Watson_Labels_Cortex.txt for the cortex and data/Paxinos_Watson_Labels.txt for the whole brain) and creates a mapping between them and the list of tissues in the SIGMA atlas using fuzzy string matching.

7. The Neurorat with SIGMA labels is then relabelled with the Paxinos Watson regions using write_paxinos_watson_regions_to_neurorat.py (run from the terminal)

8. Next, the script mask_neurorat_and_paxinos_watson.py is run from the terminal. This script creates a mask of the Neurorat, and of the Paxinos Watson atlas, in which only background and non-background are distinguished.

9. The masked image created in step 8 is aligned to the Paxinos Watson atlas using create_transform_neurorat_to_paxinos_watson.sh. This script loads the Paxinos Watson atlas (data/Paxinos_Watson_Atlas.nii.gz), the Neurorat with Paxinos Watson labels, and the masks for each of these two atlases, and uses FSL FLIRT to align the Neurorat to the Paxinos Watson atlas.

10. The transform calculated in the previous step is applied to the Neurorat label field using transform_neurorat_to_paxinos_watson_space.sh. This script first calls convert_to_ants_transform_neurorat_to_paxinos_watson.py, which loads the FSL transformation matrix that maps the Neurorat to the Paxinos Watson atlas, and writes it as an ANTs transform.

The script then resizes the Paxinos Watson atlas to match the size of the Neurorat (data/Neurorat.nii.gz) plus 100 pixels of padding.

The script transform_neurorat_to_paxinos_watson_space.sh then loads the Neurorat head label field (data/Neurorat.nii.gz), and the padded Paxinos Watson image, and aligns the former to the latter using the ANTs transform generated by convert_to_ants_transform_neurorat_to_paxinos_watson.py.

This step also applies a scaling of 0.96875 in order to match the juvenile rat.

## Citation
If you use this software, we kindly ask you to cite the following publication: BlueRecording: A Pipeline for efficient calculation of extracellular recordings in large-scale neural circuit models

## Acknowledgment
The development of this software was supported by funding to the Blue Brain Project, a research center of the École polytechnique fédérale de Lausanne (EPFL), from the Swiss government's ETH Board of the Swiss Federal Institutes of Technology.

Copyright (c) 2023 Blue Brain Project/EPFL
