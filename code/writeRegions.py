import ants
import numpy as np
import time 

im = ants.image_read('../data/SIGMA_Anatomical_Brain_Atlas.nii')

newRegions = np.load('../intermediateFiles/matchRegions.npy')

imvals = im.numpy()
s = np.shape(imvals)
imvals = imvals.flatten()

vals  = np.unique(imvals)

newvals = np.zeros_like(imvals)

for i,val in enumerate(vals):

    idx = np.where(newRegions[:,0]==val)
    newval = newRegions[idx,1]+1
    idxs = np.where(imvals==val)
    newvals[idxs]=newval

newvals = np.reshape(newvals,s)
fem = im.new_image_like(newvals)

ants.image_write(fem,'../intermediateFiles/sig_with_paxRegions.nii.gz')
