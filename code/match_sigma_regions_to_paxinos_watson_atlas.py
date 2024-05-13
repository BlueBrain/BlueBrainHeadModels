# SPDX-License-Identifier: Apache-2.0
from thefuzz import process,fuzz
import numpy as np 

paxDat = np.genfromtxt('../data/Paxinos_Watson_Labels_Cortex.txt',delimiter='\t',dtype=str) # List of tissues in paxinos-watson atlas, cortex only
sigDat = np.genfromtxt('../data/SIGMA_Anatomical_Brain_Atlas_Labels.txt', skip_header=14,delimiter='\t',dtype=str) # List of tissues in SIGMA atlas

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

newPaxDat = np.genfromtxt('../data/Paxinos_Watson_Labels.txt',delimiter='\t',dtype=str) # List of tissues in paxinos_watson atlas
for pax in newPaxDat:
    paxNums.append(pax[0])
    paxNames.append(pax[-1])

pairs = []



for i, name in enumerate(sigNames):
    
    match = process.extractOne(name,paxNames,scorer=fuzz.token_sort_ratio)[0]
    idx = paxNames.index(match)

    oldNum = sigNums[i].astype(int)
    matchNum = paxNums[idx].astype(int)
    pairs.append([oldNum,matchNum])

np.save('../intermediateFiles/matchRegions_SigmaToPW.npy',pairs) # Pairs of tissue numbers for corresponding tissues in each atlas
