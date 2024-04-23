# BlueBrainHeadModels

This repository contains scripts used to generate a finite element model of a rat head aligned to the Blue Brain Project Somatosensory cortex model.

## Dependencies and configuration instructions

This pipeline depends on ANTs Version: 2.3.4.dev206-g2251c, and on fsl flirt version 6.0, both of which must be installed by the user. The user must ensure that FSL is available from the command line (e.g., by modifying their ~/.bash_profile file) for this pipeline to work. 

This pipeline also depends on the python packages listed in the requirements.txt file, which can be pip installed. 

You will have to update the paths to your ANTs installation and to the location of your pip virtual environment in the bash scripts, and in code/align_waxholm_to_neurorat/config.py. When running python scripts from the terminal, please ensure you have your virtual environment active

This pipeline was run on a CentOS Linux cluster with the slurm job submission system; the bash scripts assume that this is true of your system as well. 

## Input data

This pipeline aligns the  ViZOO NeuroRat (150g) model V4.0 (DOI: 10.13099/VIP91106-04-1, https://itis.swiss/virtual-population/animal-models/animals/neurorat/) to the Paxinos Watson atlas. In intermediate steps, it uses the SIGMA atlas (https://www.nitrc.org/projects/sigma_template) and the Waxholm Atlas (https://www.nitrc.org/projects/whs-sd-atlas). 

All input data can be downloaded from 10.5281/zenodo.10926947. Except for the zip file described in the next paragraph, all of the files should be saved to the *data* folder before beginning the workflow.

Download and unzip the folder *align_waxholm_to_neurorat.zip* from the Zenodo repository, and copy it to the folder *data/align_waxholm_to_neurorat* in this repo.

## Workflow

### Relabel SIGMA atlas with regions from Waxholm atlas

1. A mapping from SIGMA atlas labels to Waxholm atlas labels is created semi-automatically with code/match_waxholm_regions_to_sigma_atlas.py (run from the terminal). This function loads the lists of tissues for the Waxholm atlas (data/Waxholm_Atlas_Labels.txt) and for the SIGMA atlas (data/SIGMA_Anatomical_Brain_Atlas_Labels.txt) and creates a mapping between them using fuzzy string matching. For each pair, the user must either accept the match, by entering the return key, or provide an alternative region name. The mapping used in the paper is provided in (intermediateFiles/matchRegions.npy)

2. A relabelled SIGMA atlas is written using code/write_waxholm_regions_to_sigma_atlas.py (run from the terminal). This script loads the original SIGMA atlas (data/SIGMA_Anatomical_Brain_Atlas.nii) and replaces its labels with the Waxholm labels from the previous step.

### Register SIGMA atlas to Waxholm space

3. The relabelled SIGMA atlas is masked using code/mask_sigma_atlas.py (run from the terminal). This script creates a copy of the relabelled SIGMA atlas, in which only background and non-background are distinguished.

4. The relabelled SIGMA atlas label field is mapped to the Waxholm atlas using code/create_transform_sigma_to_waxholm.sh. This script uses FSL FLIRT to align the relabeled SIGMA atlas to the Waxholm atlas (data/Waxholm_Atlas.nii.gz). The mask of the SIGMA atlas, calculated in the previous step, is also used as an input to this step.

### Register Waxholm atlas to NeuroRat space

5. Run the scrpit code/align_waxholm_to_neurorat/mask.py (from the terminal). This script creates a binary mask for the NeuroRat model label field (data/align_waxholm_to_neurorat/NeuroRatLabels.nii.gz)

6. Run the script code/align_waxholm_to_neurorat/register.sh. This script launches align_waxholm_to_neurorat/register_waxholm2aic.py, which creates a nonlinear alignment between the Waxholm atlas (data/align_waxholm_to_neurorat/Waxholm_Atlas_MRI.nii.gz) and the NeuroRat atlas (data/align_waxholm_to_neurorat/NeuroRat_MRI.nii.gz)

### Register SIGMA Atlas to NeuroRat space

7. The script code/transform_sigma_atlas_to_neurorat_space.sh is run next. This first calls the script code/convert_to_ants_transform_sigma_to_waxholm.py, which converts the FSL transformation matrix from step 4 to an ANTs transformation matrix. code/transform_sigma_atlas_to_neurorat_space.sh then applies the ANTs transformation to the original SIGMA atlas; this produces a model in Waxholm space with the original SIGMA labels. It then aligns the SIGMA-labeled Waxholm rat to the NeuroRat using the transform calculated in step 6 (intermediateFiles/transform_waxholm_to_neurorat.h5)

### Relabel NeuroRat with regions from Paxinos-Watson atlas

8. The mapping from the SIGMA labels to the Paxinos-Watson labels is calculated using the script **code/match_sigma_regions_to_paxinos_watson_atlas.py** (run from the terminal). This loads the lists of tissues for the Paxinos Watson atlas (data/Paxinos_Watson_Labels_Cortex.txt for the cortex and data/Paxinos_Watson_Labels.txt for the whole brain) and creates a mapping between them and the list of tissues in the SIGMA atlas using fuzzy string matching.

9. The SIGMA-labelled model in NeuroRat space (produced at the end of step 7) is then relabelled with the Paxinos Watson regions using code/write_paxinos_watson_regions_to_neurorat.py (run from the terminal)

### Register NeuroRat to Paxinos-Watson space

10. Next, the script code/mask_neurorat_and_paxinos_watson.py is run from the terminal. This script creates a mask of the NeuroRat, and of the Paxinos Watson atlas, in which only background and non-background are distinguished.

11. The masked image created in step 10 is aligned to the Paxinos Watson atlas using code/create_transform_neurorat_to_paxinos_watson.sh. This script loads the Paxinos Watson atlas (data/Paxinos_Watson_Atlas.nii.gz), the NeuroRat with Paxinos Watson labels (created in step 9), and the masks for each of these two atlases, and uses FSL FLIRT to align the Neurorat to the Paxinos Watson atlas.

12. The transform calculated in the previous step is applied to the Neurorat label field using code/transform_neurorat_to_paxinos_watson_space.sh. This script first calls code/convert_to_ants_transform_neurorat_to_paxinos_watson.py, which loads the FSL transformation matrix that maps the Neurorat to the Paxinos Watson atlas, and writes it as an ANTs transform. The script then resizes the Paxinos Watson atlas to match the size of the Neurorat (data/Neurorat.nii.gz) plus 100 pixels of padding. The script code/transform_neurorat_to_paxinos_watson_space.sh. then loads the Neurorat head label field (data/Neurorat.nii.gz),  the padded Paxinos Watson image, and aligns the former to the latter using the ANTs transform generated by code/convert_to_ants_transform_neurorat_to_paxinos_watson.py. This step also applies a scaling of 0.96875 in order to match the juvenile rat.

## Citation
If you use this software, we kindly ask you to cite the following publication: BlueRecording: A Pipeline for efficient calculation of extracellular recordings in large-scale neural circuit models

## Acknowledgment
The development of this software was supported by funding to the Blue Brain Project, a research center of the École polytechnique fédérale de Lausanne (EPFL), from the Swiss government's ETH Board of the Swiss Federal Institutes of Technology.

Copyright (c) 2023 Blue Brain Project/EPFL
