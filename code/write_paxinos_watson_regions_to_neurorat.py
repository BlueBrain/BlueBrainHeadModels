import ants
import numpy as np

im = ants.image_read('../intermediateFiles/sigLabelsAlignedToOsparc.nii.gz') # SIGMA atlas aligned to osparc rat, produced by transform.sh

newRegions = np.load('../intermediateFiles/matchRegions_SigmaToPW.npy') # List of corresponding tissues between sigma and paxinos-watson atlas

imvals = im.numpy()
s = np.shape(imvals)
imvals = imvals.flatten()

vals  = np.unique(imvals) # List of tissues in sigma atlas

newvals = np.zeros_like(imvals)

for i,val in enumerate(vals):

    idx = np.where(newRegions[:,0]==val) 
    newval = newRegions[idx,1] # Finds corresponding tissue in paxinos-watson atlas
    idxs = np.where(imvals==val)
    newvals[idxs]=newval # Replaces sigma labels with paxinos-watson labels

newvals = np.reshape(newvals,s)
fem = im.new_image_like(newvals)

ants.image_write(fem,'../intermediateFiles/paxLabelsAlignedToOsparc.nii.gz') # OSPARC atlas with paxinos-watson labels
