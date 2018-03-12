import pickle
import numpy as np


def get_sets(filename):
    protid = []
    structures = []
    with open(filename, "r") as fh:
        lines = fh.readlines()
        for line in range(0, len(lines)-3, 3):
            protid.append(lines[line][1:].strip())
            structures.append(lines[line+2].strip())
    return protid, structures


def feature_vecs (protid,  window):
    
    pssmdict = pickle.load(open("all_scripts/python/PSSMdict_large.sav", "rb"))
    paddingmtx = np.zeros((window//2, 20))
    offset = window // 2  

    seq_vec = []
    for prot in protid:
        pssm = pssmdict[prot]
        pssm = np.append(pssm, paddingmtx, axis=0)
        pssm = np.append(paddingmtx, pssm, axis=0)     
        for i in range(offset, pssm.shape[0]-offset):
            features = pssm[i-offset : i+offset+1].flatten()
            seq_vec = seq_vec.append(features)

    pickle.dump(seq_vec, open(dumps, "wb"))
            
    

    

if __name__ == "__main__":
    for window in range ((13,23), 2)
        window = window 
        dumps = "seq_vec"+window+".sav"
        protid, structures = (get_sets("datasets/3sstride_full.txt"))  
        feature_vecs(protid, window)
    
    print("all done")
