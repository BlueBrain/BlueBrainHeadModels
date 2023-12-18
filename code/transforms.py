import ants
import numpy as np
import scipy.io as sio

matrix = np.loadtxt('matrix.mat')

ref = ants.image_read('/gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/WHS_atlas_prealigned.nii.gz')

mov = ants.image_read('/gpfs/bbp.cscs.ch/project/proj45/scratch/newRegistration/sig_with_paxRegions.nii.gz')
#mov = ants.image_read('/gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/fem_with_paxRegionsColorMaskiCrop.nii.gz')

t = ants.fsl2antstransform(matrix,ref,mov)

#out = t.apply_to_image(mov,reference=ref)#,interpolation='nearestNeighbor')

ants.write_transform(t,'transform.mat')

#out = ants.apply_transforms(ref,mov,['matrix.mat'])

#ants.image_write(out,'output2.nii.gz')
