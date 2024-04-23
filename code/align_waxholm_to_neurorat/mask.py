import ants
import numpy as np

im = ants.image_read('../../data/align_waxholm_to_neurorat/NeuroRatLabels.nii.gz')


maskvals = 3. # Background
imvals = im.numpy()

imvals[np.where(imvals!=maskvals)]=1 # Regions that are not background are set to 1

imvals[np.where( imvals==maskvals )]=0 # Background is set to 0

masked = im.new_image_like(imvals)

ants.image_write(masked,'../../intermediateFiles/NeuroRatMask.nii.gz') # Mask
