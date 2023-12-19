import ants
import numpy as np
import scipy.io as sio

matrix = np.loadtxt('../intermediateFiles/matrixSigmaToWaxholm_FSL.mat') #FSL Transformation matrix aligning SIGMA to waxholm atlas, produced by mapSigToWax.sh

ref = ants.image_read('../data/WHS_atlas_prealigned.nii.gz') # Waxholm atlas

mov = ants.image_read('../intermediateFiles/sig_with_waxRegions.nii.gz') # Sigma atlas with Waxholm regions, produced by writeRegions.py

t = ants.fsl2antstransform(matrix,ref,mov)


ants.write_transform(t,'../intermediateFiles/transformSigmaToWaxholm_ANTS.mat') # ANTs transformation matrix

