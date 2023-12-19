import ants
import numpy as np
import scipy.io as sio

matrix = np.loadtxt('pwMatrix.mat')

ref = ants.image_read('/gpfs/bbp.cscs.ch/project/proj68/home/bolanos/Paxinos/raw/NII/PW_RBSC_6th_indexed_volume.nii.gz')

mov = ants.image_read('/gpfs/bbp.cscs.ch/project/proj45/scratch/newRegistration/paxLabelsAlignedToOsparcMasked.nii.gz')

i = ants.image_read('/gpfs/bbp.cscs.ch/project/proj45/scratch/newRegistration/20200810_segmentation_cropped.nii.gz')

t = ants.fsl2antstransform(matrix,ref,mov)

ants.write_transform(t,'transformFullMesh.mat')

size = np.max(np.shape(i.numpy()))+100
newref = ants.pad_image(ref,pad_width=[size,size,size])
ants.image_write(newref,'/gpfs/bbp.cscs.ch/project/proj45/scratch/newRegistration/PW_RBSC_6th_indexed_volume_pad_full.nii.gz')
