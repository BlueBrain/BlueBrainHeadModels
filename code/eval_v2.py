import ants
import numpy as np


im = ants.image_read('../intermediateFiles/paxLabelsAlignedToOsparc.nii.gz') # OSPARC atlas with paxinos-watson labels, created by writeRegionsPW.py


newvals = im.numpy()


newvals[np.where(newvals==866)]=0 # Sets background to 0


paxlabels = im.new_image_like(newvals)

newvals[np.where(newvals!=0)]=1


binarymask = im.new_image_like(newvals)
paxlabels = ants.crop_image(paxlabels,label_image=binarymask)


sscx = np.array([721,722,723,724,725,726,727,728,730,731])

newvalscopy = im.numpy()
newvalscopy[np.where(~np.isin(newvalscopy,sscx))]=6
newvalscopy[np.where(np.isin(newvalscopy,sscx))]=11 # Sets  Sscx to 1

newvalscopy[np.where(newvals==0)]=0 # Sets background to 0


sscxmask = im.new_image_like(newvalscopy)
newerimage = ants.crop_image(sscxmask,label_image=binarymask)

#ants.image_write(binarymask,'../intermediateFiles/paxLabelsAlignedToOsparcBinaryMask.nii.gz')
#ants.image_write(paxlabels,'../intermediateFiles/paxLabelsAlignedToOsparcMasked.nii.gz') # Osparc rat with paxinos-watson labels, with mask applied
ants.image_write(newerimage,'../intermediateFiles/paxLabelsAlignedToOsparcMask_v2.nii.gz') # Mask of osparc rat

im = ants.image_read('../data/PW_RBSC_6th_indexed_volume.nii.gz') #Paxinos-watson atlas


newvals = im.numpy()


newvalscopy = im.numpy()

newvalscopy[np.where(newvalscopy!=0)]=1 
binarymask = im.new_image_like(newvalscopy)

newvals[np.where(~np.isin(newvals,sscx))]=6
newvals[np.where(np.isin(newvals,sscx))]=11 # Sets sscx to 1
newvals[np.where(newvalscopy==0)]=0

newimage = im.new_image_like(newvals)

ants.image_write(newimage,'../intermediateFiles/PWMaskMask_v2.nii.gz') # Mask of paxinos-watson atlas
#ants.image_write(binarymask,'../intermediateFiles/PWMaskBinary.nii.gz') # Mask of paxinos-watson atlas

