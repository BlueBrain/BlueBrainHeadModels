import ants
import numpy as np
import scipy.io as sio

matrix = np.loadtxt('../intermediateFiles/pwMatrix.mat')#FSL Transformation matrix aligning osparc to paxinos-watson atlas, produced by mapSigToWax.sh

newMat = np.matmul(np.array([[.92,0,0,0],[0,.92,0,0],[0,0,.92,0],[0,0,0,1]]),matrix) # Adds scaling factor of 0.92 to account for age of BBP rat compared to PW rat

ref = ants.image_read('../data/PW_RBSC_6th_indexed_volume.nii.gz') # Paxinos-watson atlas

mov = ants.image_read('../intermediateData/paxLabelsAlignedToOsparcMasked.nii.gz')

i = ants.image_read('../data/Crop-20210802.nii.gz') # Cropped head of the osparc rat

size = np.shape(i.numpy())
s = [(500,500),(1500,500),(500,500)]

newref = ants.pad_image(ref,pad_width=s) # Adds padding to paxinos-watson atlas
ants.image_write(newref,'../intermediateFiles/PW_RBSC_6th_indexed_volume_pad_full.nii.gz')

t = ants.fsl2antstransform(newMat,newref,mov)
ants.write_transform(t,'transformFullMesh.mat') #ANTs Transformation matrix aligning osparc to paxinos-watson atlas
