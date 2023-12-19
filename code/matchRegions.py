from fuzzywuzzy import process,fuzz
import numpy as np 

paxDat = np.loadtxt('../data/whs_sd_tissuelist.txt',dtype=str)
sigDat = np.genfromtxt('../data/SIGMA_Anatomical_Brain_Atlas_Labels.txt', skip_header=14,delimiter='\t',dtype=str)

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


for i, name in enumerate(sigNames):
    
    match = process.extractOne(name,paxNames,scorer=fuzz.token_sort_ratio)[0]
    
    
    m = input()
    if m != '':
        match = m

    idx = paxNames.index(match)
    oldNum = sigNums[i].astype(int)
    matchNum = paxNums[idx].astype(int)+1
    pairs.append([oldNum,matchNum])

   

np.save('../intermediateFiles/matchRegions.npy',pairs)
