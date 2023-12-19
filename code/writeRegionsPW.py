import ants
import numpy as np
import time 

im = ants.image_read('../intermediateFiles/sigLabelsAlignedToOsparc.nii.gz')

newRegions = np.load('../intermediateFiles/matchRegions_SigmaToPW.npy')

imvals = im.numpy()
s = np.shape(imvals)
imvals = imvals.flatten()

vals  = np.unique(imvals)

newvals = np.zeros_like(imvals)

for i,val in enumerate(vals):

    idx = np.where(newRegions[:,0]==val)
    newval = newRegions[idx,1]
    idxs = np.where(imvals==val)
    newvals[idxs]=newval

newvals = np.reshape(newvals,s)
fem = im.new_image_like(newvals)

ants.image_write(fem,'../intermediateFiles/paxLabelsAlignedToOsparc.nii.gz')
