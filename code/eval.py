import ants
import numpy as np
import time

#m = ants.image_read('/gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/osparc_rat_mri.nrrd')
#ants.image_write(m, '/gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/oscparc_rat_mri.nii.gz')

#im = ants.image_read('/gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/masked.nrrd')
#ants.image_write(im, '/gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/masked.nii.gz')

#im = ants.image_read('/gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/fem_with_paxRegions.nrrd')
#ants.image_write(im, '/gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/fem_with_paxRegions.nii.gz')

#orig = ants.image_read('/gpfs/bbp.cscs.ch/home/tharayil/build/shlabel2epi0pad.nii.gz')
#origvals = orig.numpy()

#pts = np.where(origvals==522)

#origvals[pts]=722

#fem = orig.new_image_like(origvals)

#ants.image_write(fem,'test.nii.gz')
#new = ants.image_read('test.nii.gz')
#newvals = new.numpy()
#newpts = np.where(newvals==722)
#print(newpts)
#new = ants.image_read('/gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/fem_with_paxRegions.nii.gz')
#newvals = new.numpy()
#newpts = np.where(newvals ==722)

#print(newpts)

#im = ants.image_read('/gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/atlas_with_paxRegions.nii.gz')
#imvals = im.numpy()
#imvals[np.where(imvals==866)]=0

#ants.image_write(im.new_image_like(imvals), '/gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/fem_with_paxRegionsColor.nii.gz')

im = ants.image_read('/gpfs/bbp.cscs.ch/project/proj45/scratch/newRegistration/paxLabelsAlignedToOsparc.nii.gz')

vals = np.unique(im.numpy())

newvals = im.numpy()
newvals[np.where(newvals==866)]=0


newimage = im.new_image_like(newvals)

newvals[np.where(newvals!=0)]=1
newerimage = im.new_image_like(newvals)
newimage = ants.crop_image(newimage,label_image=newerimage)
newerimage = ants.crop_image(newerimage,label_image=newerimage)
ants.image_write(newimage,'/gpfs/bbp.cscs.ch/project/proj45/scratch/newRegistration/paxLabelsAlignedToOsparcMasked.nii.gz')
ants.image_write(newerimage,'/gpfs/bbp.cscs.ch/project/proj45/scratch/newRegistration/paxLabelsAlignedToOsparcMask.nii.gz')

#im = ants.image_read('/gpfs/bbp.cscs.ch/project/proj68/home/bolanos/Paxinos/raw/NII/PW_RBSC_6th_indexed_volume.nii.gz')

#vals = np.unique(im.numpy())

#newvals = im.numpy()
#newvals[np.where(newvals!=0)]=1


#newimage = im.new_image_like(newvals)
#newerimage = ants.crop_image(im,label_image=newimage)
#ants.image_write(newimage,'/gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/PWMaskMask.nii.gz')

#print(1)
#newRegions = np.load('/gpfs/bbp.cscs.ch/home/tharayil/build/matchRegions.npy')
#print(2)
#imvals = im.numpy()
#print(3)
#t = time.time()
#import ants
#import numpy as np
#
#im = ants.image_read( 'shlabel2epi0pad.nii.gz'  )


#m = im.numpy()
#print(np.unique(m))
