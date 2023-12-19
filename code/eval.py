import ants
import numpy as np
import time


im = ants.image_read('/gpfs/bbp.cscs.ch/project/proj45/scratch/newRegistration/paxLabelsAlignedToOsparc.nii.gz') # OSPARC atlas with paxinos-watson labels, created by writeRegionsPW.py

vals = np.unique(im.numpy()) # List of paxinos-watson labels

newvals = im.numpy()
newvals[np.where(newvals==866)]=0 # Sets background to 0


newimage = im.new_image_like(newvals)

newvals[np.where(newvals!=0)]=1 # Sets non-background regions to 1

newerimage = im.new_image_like(newvals)

newimage = ants.crop_image(newimage,label_image=newerimage)

newerimage = ants.crop_image(newerimage,label_image=newerimage)

ants.image_write(newimage,'../intermediateData/paxLabelsAlignedToOsparcMasked.nii.gz') # Osparc rat with paxinos-watson labels, with mask applied
ants.image_write(newerimage,'../intermediateData/paxLabelsAlignedToOsparcMask.nii.gz') # Mask of osparc rat

im = ants.image_read('../data/PW_RBSC_6th_indexed_volume.nii.gz') #Paxinos-watson atlas

vals = np.unique(im.numpy()) # List of values in paxinos-watson atlas

newvals = im.numpy()
newvals[np.where(newvals!=0)]=1 # Sets non-background values to 1


newimage = im.new_image_like(newvals)
newerimage = ants.crop_image(im,label_image=newimage)
ants.image_write(newimage,'../intermediateData/PWMaskMask.nii.gz') # Mask of paxinos-watson atlas

