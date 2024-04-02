import ants
import numpy as np

im = ants.image_read('../intermediateFiles/sig_with_waxRegions.nii.gz') # SIGMA atlas with Waxholm regions, produced by writeRegions.py


maskvals = 7. # Background
imvals = im.numpy()

imvals[np.where(imvals!=maskvals)]=1 # Regions that are not background are set to 1

imvals[np.where( imvals==maskvals )]=0 # Background is set to 0

masked = im.new_image_like(imvals)

ants.image_write(masked,'../intermediateFiles/mask.nii.gz') # Mask of SIGMA atlas
