import ants
import numpy as np
import scipy.io as sio

matrix = np.loadtxt('../intermediateFiles/matrixSigmaToWaxholm_FSL.mat')

ref = ants.image_read('../data/WHS_atlas_prealigned.nii.gz')

mov = ants.image_read('../intermediateFiles/sig_with_paxRegions.nii.gz')

t = ants.fsl2antstransform(matrix,ref,mov)


ants.write_transform(t,'../intermediateFiles/transformSigmaToWaxholm_ANTS.mat')

