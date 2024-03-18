from fuzzywuzzy import process,fuzz
import numpy as np 

waxDat = np.loadtxt('../data/whs_sd_tissuelist.txt',dtype=str) # List of tissues in waxholm atlas
sigDat = np.genfromtxt('../data/SIGMA_Anatomical_Brain_Atlas_Labels.txt', skip_header=14,delimiter='\t',dtype=str) # List of tissues in sigma atlas

sigNums = []
sigNames = []
for sig in sigDat:
    sigNums.append(sig[0])
    sigNames.append(sig[-1])

waxNums  = []
waxNames = []
for wax in waxDat:
    waxNames.append(wax)

waxNums = np.arange(len(waxNames))

pairs = []


for i, name in enumerate(sigNames):
    
    match = process.extractOne(name,waxNames,scorer=fuzz.token_sort_ratio)[0] # Result obtained by fuzzy string matching
    
    print(name)
    print(match)
    
    m = input('Press ENTER to accept match. Otherwise, enter your own waxholm label for this sigma label') # Waits for user input. If input is '', then accepts automatic result. Otherwise, uses user input as match
    if m != '':
        match = m

    idx = waxNames.index(match)
    oldNum = sigNums[i].astype(int)
    matchNum = waxNums[idx].astype(int)+1
    pairs.append([oldNum,matchNum])

np.save('../intermediateFiles/matchRegions.npy',pairs) # Pairs of tissue numbers for corresponding tissues in each atlas
