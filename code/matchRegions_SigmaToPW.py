from fuzzywuzzy import process,fuzz
import numpy as np 

paxDat = np.genfromtxt('/gpfs/bbp.cscs.ch/project/proj68/home/bolanos/Paxinos/raw/NII/PW_RBSC_6th_cortex.txt',delimiter='\t',dtype=str)
sigDat = np.genfromtxt('/gpfs/bbp.cscs.ch/project/proj45/scratch/SIGMA_Wistar_Rat_Brain_TemplatesAndAtlases_Version1.1/SIGMA_Rat_Brain_Atlases/SIGMA_Anatomical_Atlas/SIGMA_Anatomical_Brain_Atlas_Labels.txt', skip_header=14,delimiter='\t',dtype=str)

sigNums = []
sigNames = []
for sig in sigDat:
    sigNums.append(sig[0])
    sigNames.append(sig[-1])

paxNums  = []
paxNames = []
for pax in paxDat:
    paxNums.append(pax[0])
    paxNames.append(pax[-1])

newPaxDat = np.genfromtxt('/gpfs/bbp.cscs.ch/project/proj68/home/bolanos/Paxinos/raw/NII/PW_RBSC_6th_lut.txt',delimiter='\t',dtype=str)
for pax in newPaxDat:
    paxNums.append(pax[0])
    paxNames.append(pax[-1])

pairs = []



for i, name in enumerate(sigNames):
    
    match = process.extractOne(name,paxNames,scorer=fuzz.token_sort_ratio)[0]
    idx = paxNames.index(match)#np.where(match==paxNames)
    print(name)
    print(match)
    oldNum = sigNums[i].astype(int)
    matchNum = paxNums[idx].astype(int)
    pairs.append([oldNum,matchNum])

#np.save('matchRegions.npy',pairs)
