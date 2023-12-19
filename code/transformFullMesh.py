import ants
import numpy as np
import scipy.io as sio

matrix = np.loadtxt('../intermediateData/pwMatrix.mat') #FSL Transformation matrix aligning osparc to paxinos-watson atlas, produced by mapSigToWax.sh

ref = ants.image_read('../data/PW_RBSC_6th_indexed_volume.nii.gz') # Paxinos-watson atlas

mov = ants.image_read('../intermediateData/paxLabelsAlignedToOsparcMasked.nii.gz')

i = ants.image_read('../data/20200810_segmentation_cropped.nii.gz') # Cropped head of the osparc rat

t = ants.fsl2antstransform(matrix,ref,mov)

ants.write_transform(t,'../intermediateData/transformFullMesh.mat') #ANTs Transformation matrix aligning osparc to paxinos-watson atlas

size = np.max(np.shape(i.numpy()))+100
newref = ants.pad_image(ref,pad_width=[size,size,size])
ants.image_write(newref,'../intermediateData/PW_RBSC_6th_indexed_volume_pad_full.nii.gz') # Paxinos watson atlas with padding to match the size of the osparc head, plus some margin
