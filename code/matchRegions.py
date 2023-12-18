from fuzzywuzzy import process,fuzz
import numpy as np 

paxDat = np.loadtxt('/gpfs/bbp.cscs.ch/project/proj45/scratch/osparcRat/whs_sd_tissuelist.txt',dtype=str)
sigDat = np.genfromtxt('/gpfs/bbp.cscs.ch/project/proj45/scratch/SIGMA_Wistar_Rat_Brain_TemplatesAndAtlases_Version1.1/SIGMA_Rat_Brain_Atlases/SIGMA_Anatomical_Atlas/SIGMA_Anatomical_Brain_Atlas_Labels.txt', skip_header=14,delimiter='\t',dtype=str)

sigNums = []
sigNames = []
for sig in sigDat:
    sigNums.append(sig[0])
    sigNames.append(sig[-1])

paxNums  = []
paxNames = []
for pax in paxDat:
    paxNames.append(pax)

paxNums = np.arange(len(paxNames))

pairs = []

#print(sigNames)
#print(paxNames)

for i, name in enumerate(sigNames):
    
    match = process.extractOne(name,paxNames,scorer=fuzz.token_sort_ratio)[0]
    
    print(name)
    print(match)
    
    m = input()
    if m != '':
        match = m

    idx = paxNames.index(match)
    oldNum = sigNums[i].astype(int)
    matchNum = paxNums[idx].astype(int)+1
    pairs.append([oldNum,matchNum])

   

np.save('matchRegions.npy',pairs)
