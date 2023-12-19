import ants
import numpy as np

im = ants.image_read('../intermediateFiles/sig_with_paxRegions.nii.gz')


maskvals = 7.
imvals = im.numpy()

imvals[np.where(imvals!=maskvals)]=1

imvals[np.where( imvals==maskvals )]=0

masked = im.new_image_like(imvals)

ants.image_write(masked,'../intermediateFiles/mask.nii.gz')
