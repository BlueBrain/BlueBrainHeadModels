import ants
import numpy as np


im = ants.image_read('../intermediateFiles/neurorat_with_paxinos_watson_labels.nii.gz') # NeuroRat atlas with paxinos-watson labels, created by write_paxinos_watson_regions_to_neurorat.py

vals = np.unique(im.numpy()) # List of paxinos-watson labels

newvals = im.numpy()
newvals[np.where(newvals==866)]=0 # Sets background to 0


newimage = im.new_image_like(newvals)

newvals[np.where(newvals!=0)]=1 # Sets non-background regions to 1

newerimage = im.new_image_like(newvals)

newimage = ants.crop_image(newimage,label_image=newerimage)

newerimage = ants.crop_image(newerimage,label_image=newerimage)

ants.image_write(newimage,'../intermediateFiles/neurorat_with_paxinos_watson_labels_masked.nii.gz') # NeuroRat with paxinos-watson labels, with mask applied

ants.image_write(newerimage,'../intermediateFiles/neurorat_with_paxinos_watson_labels_mask.nii.gz') # Mask of neurorat

im = ants.image_read('../data/Paxinos_Watson_Atlas.nii.gz') #Paxinos-watson atlas

vals = np.unique(im.numpy()) # List of values in paxinos-watson atlas

newvals = im.numpy()
newvals[np.where(newvals!=0)]=1 # Sets non-background values to 1


newimage = im.new_image_like(newvals)
newerimage = ants.crop_image(im,label_image=newimage)
ants.image_write(newimage,'../intermediateFiles/Paxinos_Watson_Atlas_Mask.nii.gz') # Mask of paxinos-watson atlas

