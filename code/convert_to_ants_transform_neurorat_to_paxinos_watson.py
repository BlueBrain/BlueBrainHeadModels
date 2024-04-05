import ants
import numpy as np
import scipy.io as sio

matrix = np.loadtxt('../intermediateFiles/matrixNeuroratToPaxinosWatson_FSL.mat')#FSL Transformation matrix aligning osparc to paxinos-watson atlas, produced by create_transform_neurorat_to_paxinos_watson.sh

newMat = np.matmul(np.array([[.96837,0,0,0],[0,.96837,0,0],[0,0,.96837,0],[0,0,0,1]]),matrix) # Adds scaling factor of 0.96837 to account for age of BBP rat compared to PW rat

ref = ants.image_read('../data/Paxinos_Watson_Atlas.nii.gz') # Paxinos-watson atlas

mov = ants.image_read('../intermediateFiles/neurorat_with_paxinos_watson_labels_masked.nii.gz')

i = ants.image_read('../data/Neurorat.nii.gz') # Cropped head of the NeuroRat

size = np.shape(i.numpy())
s = [(500,500),(1500,500),(500,500)]

newref = ants.pad_image(ref,pad_width=s) # Adds padding to paxinos-watson atlas
ants.image_write(newref,'../intermediateFiles/Paxinos_Watson_Atlas_padded.nii.gz')

t = ants.fsl2antstransform(newMat,newref,mov)
ants.write_transform(t,'../intermediateFiles/transformNeuroratToPaxinosWatson_ANTs.mat') #ANTs Transformation matrix aligning osparc to paxinos-watson atlas
