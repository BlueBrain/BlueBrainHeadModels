import ants
import numpy as np
import time 

im = ants.image_read('/gpfs/bbp.cscs.ch/project/proj45/scratch/SIGMA_Wistar_Rat_Brain_TemplatesAndAtlases_Version1.1/SIGMA_Rat_Brain_Atlases/SIGMA_Anatomical_Atlas/SIGMA_Anatomical_Brain_Atlas.nii')

newRegions = np.load('/gpfs/bbp.cscs.ch/project/proj45/scratch/newRegistration/matchRegions.npy')

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

ants.image_write(fem,'/gpfs/bbp.cscs.ch/project/proj45/scratch/newRegistration/sig_with_paxRegions.nii.gz')
