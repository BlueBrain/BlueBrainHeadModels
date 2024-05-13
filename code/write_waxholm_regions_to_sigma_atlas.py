# SPDX-License-Identifier: Apache-2.0
import ants
import numpy as np

im = ants.image_read('../data/SIGMA_Anatomical_Brain_Atlas.nii') # SIGMA atlas

newRegions = np.load('../intermediateFiles/matchRegions.npy') # List of tissue number correspondences between SIGMA and Waxholm atlas, produced by match_waxholm_regions_to_sigma_atlas.py

imvals = im.numpy() # Atlas to numpy array
s = np.shape(imvals)
imvals = imvals.flatten()

vals  = np.unique(imvals) # Tissues in SIGMA atlas

newvals = np.zeros_like(imvals)

for i,val in enumerate(vals):

    idx = np.where(newRegions[:,0]==val) # Finds tissue in list of correspondences
    newval = newRegions[idx,1]+1 # Finds corresponding Waxholm tissue, adding 1 since they are not zero-indexed
    idxs = np.where(imvals==val)
    newvals[idxs]=newval # Replaces with Waxholm tissue

newvals = np.reshape(newvals,s)
fem = im.new_image_like(newvals)

ants.image_write(fem,'../intermediateFiles/sigma_atlas_with_waxholm_labels.nii.gz') #SIGMA atlas with Waxholm labels
