import ants
import numpy as np

im = ants.image_read('/gpfs/bbp.cscs.ch/project/proj45/scratch/newRegistration/sig_with_paxRegions.nii.gz')


#masked = ants.mask_image(im,mask,level=levels)

maskvals = 7.
imvals = im.numpy()

imvals[np.where(imvals!=maskvals)]=1

imvals[np.where( imvals==maskvals )]=0

masked = im.new_image_like(imvals)

ants.image_write(masked,'/gpfs/bbp.cscs.ch/project/proj45/scratch/newRegistration/mask.nii.gz')
