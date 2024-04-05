import ants
import numpy as np
import scipy.io as sio

matrix = np.loadtxt('../intermediateFiles/matrixSigmaToWaxholm_FSL.mat') #FSL Transformation matrix aligning SIGMA to waxholm atlas, produced by create_transform_sigma_to_waxholm.sh

ref = ants.image_read('../data/Waxholm_Atlas.nii.gz') # Waxholm atlas

mov = ants.image_read('../intermediateFiles/sigma_atlas_with_waxholm_labels.nii.gz') # Sigma atlas with Waxholm labels, produced by write_waxholm_regions_to_sigma_atlas.py

t = ants.fsl2antstransform(matrix,ref,mov)


ants.write_transform(t,'../intermediateFiles/transformSigmaToWaxholm_ANTS.mat') # ANTs transformation matrix

